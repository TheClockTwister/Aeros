from hypercorn.asyncio.run import *
from hypercorn.asyncio.run import _run, _share_socket, _windows_signal_support


async def worker_serve(
        app: ASGIFramework,
        config: Config,
        *,
        sockets: Optional[Sockets] = None,
        shutdown_trigger: Optional[Callable[..., Awaitable[None]]] = None,
) -> None:
    config.set_statsd_logger_class(StatsdLogger)

    lifespan = Lifespan(app, config)
    lifespan_task = asyncio.ensure_future(lifespan.handle_lifespan())

    await lifespan.wait_for_startup()
    if lifespan_task.done():
        exception = lifespan_task.exception()
        if exception is not None:
            raise exception

    if sockets is None:
        sockets = config.create_sockets()

    loop = asyncio.get_event_loop()
    tasks = []
    if platform.system() == "Windows":
        tasks.append(loop.create_task(_windows_signal_support()))

    if shutdown_trigger is None:
        shutdown_trigger = asyncio.Future
    tasks.append(loop.create_task(raise_shutdown(shutdown_trigger)))

    if config.use_reloader:
        tasks.append(loop.create_task(observe_changes(asyncio.sleep)))

    ssl_handshake_timeout = None
    if config.ssl_enabled:
        ssl_context = config.create_ssl_context()
        ssl_handshake_timeout = config.ssl_handshake_timeout

    async def _server_callback(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            await TCPServer(app, loop, config, reader, writer)
        except ConnectionAbortedError:
            pass

    servers = []
    for sock in sockets.secure_sockets:
        if config.workers > 1 and platform.system() == "Windows":
            sock = _share_socket(sock)

        servers.append(
            await asyncio.start_server(
                _server_callback,
                backlog=config.backlog,
                loop=loop,
                ssl=ssl_context,
                sock=sock,
                ssl_handshake_timeout=ssl_handshake_timeout,
            )
        )
        bind = repr_socket_addr(sock.family, sock.getsockname())
        await config.log.info(f"Running on {bind} over https (CTRL + C to quit)")

    for sock in sockets.insecure_sockets:
        if config.workers > 1 and platform.system() == "Windows":
            sock = _share_socket(sock)

        servers.append(
            await asyncio.start_server(
                _server_callback, backlog=config.backlog, loop=loop, sock=sock
            )
        )
        bind = repr_socket_addr(sock.family, sock.getsockname())
        await config.log.info(f"Running on {bind} over http (CTRL + C to quit)")

    for sock in sockets.quic_sockets:
        if config.workers > 1 and platform.system() == "Windows":
            sock = _share_socket(sock)

        await loop.create_datagram_endpoint(lambda: UDPServer(app, loop, config), sock=sock)
        bind = repr_socket_addr(sock.family, sock.getsockname())
        await config.log.info(f"Running on {bind} over quic (CTRL + C to quit)")

    reload_ = False
    try:
        gathered_tasks = asyncio.gather(*tasks)
        await gathered_tasks

    except MustReloadException:
        reload_ = True
    except (Shutdown, KeyboardInterrupt):
        pass
    finally:
        for server in servers:
            server.close()
            await server.wait_closed()

        # Retrieve the Gathered Tasks Cancelled Exception, to
        # prevent a warning that this hasn't been done.
        gathered_tasks.exception()

        await lifespan.wait_for_shutdown()
        lifespan_task.cancel()
        await lifespan_task

    if reload_:
        restart()


def asyncio_worker(app, config: Config, sockets: Optional[Sockets] = None, shutdown_event: Optional[EventType] = None) -> None:
    shutdown_trigger = None
    if shutdown_event is not None:
        shutdown_trigger = partial(check_multiprocess_shutdown_event, shutdown_event, asyncio.sleep)

    if config.workers > 1 and platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore

    _run(
        partial(worker_serve, app, config, sockets=sockets),
        debug=config.debug,
        shutdown_trigger=shutdown_trigger,
    )

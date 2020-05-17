from hypercorn.asyncio.run import *
from hypercorn.asyncio.run import _run


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

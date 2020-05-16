import platform
import random
import time
from multiprocessing import Event, Process

from hypercorn.config import Config
from hypercorn.typing import WorkerFunc
from hypercorn.utils import write_pid_file


def run(config):
    if config.pid_path is not None:
        write_pid_file(config.pid_path)

    worker_func: WorkerFunc
    if config.worker_class == "asyncio":
        from hypercorn.asyncio.run import asyncio_worker

        worker_func = asyncio_worker
    elif config.worker_class == "uvloop":
        from hypercorn.asyncio.run import uvloop_worker

        worker_func = uvloop_worker
    elif config.worker_class == "trio":
        from hypercorn.trio.run import trio_worker

        worker_func = trio_worker
    else:
        raise ValueError(f"No worker of class {config.worker_class} exists")

    if config.workers == 1:
        worker_func(config)
    else:
        run_multiple(config, worker_func)


def run_multiple(config: Config, worker_func: WorkerFunc) -> None:
    if config.use_reloader:
        raise RuntimeError("Reloader can only be used with a single worker")

    sockets = config.create_sockets()

    processes = []

    shutdown_event = Event()

    for _ in range(config.workers):
        process = Process(
            target=worker_func,
            kwargs={"config": config, "shutdown_event": shutdown_event, "sockets": sockets},
        )
        process.daemon = True
        process.start()
        processes.append(process)
        if platform.system() == "Windows":
            time.sleep(0.1 * random.random())

    for process in processes:
        process.join()
    for process in processes:
        process.terminate()

    for sock in sockets.secure_sockets:
        sock.close()
    for sock in sockets.insecure_sockets:
        sock.close()

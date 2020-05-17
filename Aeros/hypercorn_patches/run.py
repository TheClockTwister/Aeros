import platform
import random
import time
from multiprocessing import Event
from Aeros.threading import AdvancedThread
from hypercorn.config import Config
from hypercorn.utils import write_pid_file

from .worker import asyncio_worker


def run(app, config):
    if config.pid_path is not None:
        write_pid_file(config.pid_path)

    if config.worker_class != "asyncio":
        raise ValueError(f"No worker of class {config.worker_class} exists")

    if config.workers == 1:
        asyncio_worker(app, config)
    else:
        run_multiple(app, config, asyncio_worker)


def run_multiple(app, config: Config, worker_func: asyncio_worker) -> None:
    if config.use_reloader:
        raise RuntimeError("Reloader can only be used with a single worker")

    sockets = config.create_sockets()

    processes = []

    shutdown_event = Event()

    for _ in range(config.workers):
        process = AdvancedThread(
            target=worker_func,
            kwargs={"app": app, "config": config, "shutdown_event": shutdown_event, "sockets": sockets},
        )
        process.daemon = True
        process.start()
        processes.append(process)
        if platform.system() == "Windows":
            time.sleep(0.1 * random.random())

    for process in processes:
        process.join()
    for process in processes:
        process.stop()

    for sock in sockets.secure_sockets:
        sock.close()
    for sock in sockets.insecure_sockets:
        sock.close()

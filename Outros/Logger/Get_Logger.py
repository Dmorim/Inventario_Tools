import atexit
import datetime
import logging
import logging.handlers
import queue
from pathlib import Path


def _gerar_caminho_log() -> Path:
    agora = datetime.datetime.now()
    pasta_mes = agora.strftime("%Y%m")
    arquivo = agora.strftime("%d%m%Y_log.txt")

    base_dir = Path(__file__).resolve().parents[2] / "logs" / pasta_mes
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / arquivo


_LOG_FILE = _gerar_caminho_log()
_LOG_QUEUE = queue.Queue(-1)
_LOG_LISTENER = None


def _desligar_listener():
    global _LOG_LISTENER
    if _LOG_LISTENER is not None:
        _LOG_LISTENER.stop()
        _LOG_LISTENER = None


def _configurar_logger() -> logging.Logger:
    global _LOG_LISTENER

    logger = logging.getLogger("InventarioTools")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.handlers.TimedRotatingFileHandler(
        _LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    queue_handler = logging.handlers.QueueHandler(_LOG_QUEUE)
    logger.addHandler(queue_handler)

    _LOG_LISTENER = logging.handlers.QueueListener(
        _LOG_QUEUE,
        file_handler,
        respect_handler_level=True,
    )
    _LOG_LISTENER.start()
    atexit.register(_desligar_listener)
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    logger = _configurar_logger()
    return logger.getChild(name) if name else logger

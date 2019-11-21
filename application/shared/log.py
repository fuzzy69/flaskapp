import logging
from logging import Logger, getLogger, FileHandler, Formatter, StreamHandler, DEBUG, INFO


def create_logger(name, level=INFO,
                  log_format=("%(asctime)s [%(name)s] <%(threadName)s> %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"),
                  log_file=None) -> Logger:
    """
    Creates console and/or file logging instance
    :param str name: logger instance name, usually current python file
    :param int level: logging level, recommended DEBUG for development and INFO for production
    :param tuple log_format: tuple of outputs log message format and log time
    :param str log_file: path to log file
    :return: logging.Logger instance
    """
    logging.propagate = False
    logger = getLogger(name)
    logger.setLevel(level)
    formatter = Formatter(*log_format)
    # Remove all handlers if they exists
    logger.handlers = []
    # Console handler
    ch = StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # File handler
    if log_file is not None:
        fh = FileHandler(log_file)
        fh.setLevel(DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger



class DummyLogger:
    """"""
    def __init__(self):
        pass

    def debug(self, message: str, *args, **kwargs):
        pass

    def info(self, message: str, *args, **kwargs):
        pass

    def warning(self, message: str, *args, **kwargs):
        pass

    def error(self, message: str, *args, **kwargs):
        pass

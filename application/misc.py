import argparse
from logging import Filter, Formatter, StreamHandler, WARNING
from logging.handlers import RotatingFileHandler

from config import __description__, LOG_DIR, LOG_FILE, LOG_FORMAT


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line and return program arguments
    :return: argparse.Namespace instance
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-d", action="store_true", dest="debug", help="Run WebUI server in a development mode")
    parser.add_argument("-v", action="store_true", dest="verbose", help="Enable verbose logging")
    args, _ = parser.parse_known_args()

    return args


def setup_logging(app, log_level):
    """Sets up Flask logging and returns Flask application instance"""
    if log_level is None:
        return
    if app.logger.hasHandlers():  # Remove previous log handlers
        app.logger.handlers.clear()
    # File logging
    file_formatter = Formatter(*LOG_FORMAT)
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024 * 10)
    file_handler.setLevel(WARNING)
    file_handler.setFormatter(file_formatter)
    # Console logging
    stream_formatter = Formatter(*LOG_FORMAT)
    stream_handler = StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(stream_formatter)
    # Set up Flask logging
    app.logger.addHandler(stream_handler)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)

    return app


class StaticFilesFilter(Filter):
    """Custom logging filter"""
    def filter(self, record):
        """Removes details about static files and dynamic pages from logs"""
        show_message = True
        if "GET /static/" in record.getMessage():
            show_message = False
        elif "GET /xhr/" in record.getMessage():
            show_message = False

        return show_message

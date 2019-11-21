# -*- coding: UTF-8 -*-

import sys
from logging import DEBUG, INFO

from application.base import app
from application.common import ExitCode
from application.misc import parse_arguments, setup_logging
from application.shared.filesystem import ensure_dir

from config import LOG_DIR, HOST, PORT, SECRET_KEY


def main() -> int:
    """WebUI server main entry point. Parse provided command line arguments, setup a Flask server and run it."""
    # Command line arguments
    args = parse_arguments()
    # Create required directories if they don't exist
    ensure_dir(LOG_DIR)
    log_level = DEBUG if args.verbose else INFO
    setup_logging(app, log_level)
    if SECRET_KEY is None:
        app.logger.error("Setup you FLASKAPP_KEY environment variable first in order to run the application!")
        return ExitCode.FAILURE.value
    # Run server
    app.run(host=HOST, port=PORT, debug=DEBUG)

    return ExitCode.SUCCESS.value


if __name__ == "__main__":
    sys.exit(main())

import os
import logging
from rich.logging import RichHandler
from rich.traceback import install

install()


def create_logger():
    """create a logger for the app"""
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    rich_handler = RichHandler(
        rich_tracebacks=True, markup=True
    )
    logging.basicConfig(
        level=log_level, format='%(message)s', 
        handlers=[rich_handler], 
        datefmt=['%Y-%m-%d %H:%M:%S']
    )

    return logging.getLogger('rich')
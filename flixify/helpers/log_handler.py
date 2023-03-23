"""Log handler module"""

import logging
import os

from flixify.helpers.constants import LOG_DIR

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'main.log'),
    filemode='a',
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.DEBUG
)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


def create_logger(name, filename):
    """
    Creates a logger with the specified name and writes log messages to
    the specified file.

    :param name: The name of the logger.
    :param filename: The name of the file to which log messages should be
        written.

    :returns: The created logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, filename))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


# create logger for services application module
services_logger = create_logger('services', 'services/services.log')

# create logger for places module
dao_logger = create_logger('dao', 'dao/dao.log')

# create logger for places module
views_logger = create_logger('views', 'views/views.log')

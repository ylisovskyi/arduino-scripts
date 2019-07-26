import coloredlogs, logging


def get_logger(name):
    """Returns a logger with logging level DEBUG set and custom output format"""
    logger = logging.getLogger(name)
    coloredlogs.install(
        level='DEBUG',
        logger=logger,
        fmt='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%m-%d-%Y %H:%M:%S'
    )
    return logger

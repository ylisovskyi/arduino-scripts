import logging


def get_logger(name):
    logging.root.setLevel(logging.DEBUG)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%m-%d-%Y %H:%M:%S'
    )
    return logging.getLogger(name)

import logging

logger = logging.getLogger(__name__)

_loop = None

def set_event_loop(loop):
    global _loop
    logger.info(f"SET loop id={id(loop)}")
    _loop = loop

def get_event_loop():
    logger.info(f"GET loop -> {_loop}")
    return _loop
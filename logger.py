from datetime import date
from logging import getLogger, FileHandler, StreamHandler, Formatter, DEBUG, INFO

logger = getLogger(__name__)
logger.setLevel(DEBUG)
log_fmt = Formatter("%(asctime)s %(name)s %(lineno)d [%(levelname)s][%(funcName)s] %(message)s")

stream_handler = StreamHandler()
stream_handler.setLevel(INFO)
stream_handler.setFormatter(log_fmt)
logger.addHandler(stream_handler)

file_handler = FileHandler(filename=f"logs/{date.today()}.log", encoding="utf-8")
file_handler.setLevel(DEBUG)
file_handler.setFormatter(log_fmt)
logger.addHandler(file_handler)
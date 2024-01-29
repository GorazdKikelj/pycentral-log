from logging import Logger, getLogger, basicConfig, NOTSET, INFO, DEBUG, WARNING, ERROR, CRITICAL
from .utilities import check_path

C_LOG_DIR = "log/"
check_path(C_LOG_DIR)

logger: Logger = getLogger(__name__)
basicConfig(
    filename=f"{C_LOG_DIR}troubleshooting.log",
    filemode="a",
    format="%(asctime)s : %(levelname)s : %(module)s %(lineno)d : %(message)s",
    level=INFO,
)

log_level: dict[str, int] = {
    "NOTSET": NOTSET,
    "DEBUG": DEBUG,
    "INFO": INFO,
    "WARNING": WARNING,
    "ERROR": ERROR,
    "CRITICAL": CRITICAL,
}


def logwrite(msg: str, level: str) -> None:
    if level == "NOTSET":
        logger.log(msg, NOTSET)
    elif level == "DEBUG":
        logger.debug(msg)
    elif level == "INFO":
        logger.info(msg)
    elif level == "WARNING":
        logger.warning(msg)
    elif level == "ERROR":
        logger.error(msg)
    elif level == "CRITICAL":
        logger.critical(msg)       
    
    return None
    
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(module)s %(lineno)d : %(process)d - %(thread)d : %(message)s', level=logging.DEBUG)

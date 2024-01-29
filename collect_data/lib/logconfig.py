import logging
from lib.utilities import check_path

C_LOG_DIR = "log/"
check_path(C_LOG_DIR)

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f"{C_LOG_DIR}troubleshooting.log",
    filemode="a",
    format="%(asctime)s : %(levelname)s : %(module)s %(lineno)d : %(message)s",
    level=logging.INFO,
)

log_level = {
    "NOTSET": 0,
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(module)s %(lineno)d : %(process)d - %(thread)d : %(message)s', level=logging.DEBUG)

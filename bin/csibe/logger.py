import os
import inspect
import logging

"""
CSiBE logging facality

If CSiBE_DEBUG_FILE environmental variable is set all CRITICAL and ERROR
messages will be sent to the required file. Otherwise the messages will be sent
to stdout and stderr.

If CSiBE_DEBUG environmental variable is set to 1 all DEBUG, INFO, WARNING,
ERROR, and CRITICAL messages will be displayed.

Sample usage:
  from csibe import logger
  logger.error(error_text)
  logger.debug(debug_text)
"""

if os.getenv("CSiBE_DEBUG_FILE", ""):
    __args = {"filename": os.environ["CSiBE_DEBUG_FILE"], "level": logging.ERROR}
else:
    __args = {"level": logging.CRITICAL}
__frame = inspect.stack()[2]
__module = inspect.getmodule(__frame[0])
logging.basicConfig(**__args)

"""The main logger facality for CSiBE"""
logger = logging.getLogger(__module.__file__)

if os.getenv("CSiBE_DEBUG", "") == "1":
    logger.setLevel(logging.DEBUG)

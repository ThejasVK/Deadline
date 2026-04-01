"""
Comprehensive logging system for DOIT backend
Logs all actions with timestamps to a single file
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path("/Users/thejasvk/Documents/Projects/Deadline/logs")
LOGS_DIR.mkdir(exist_ok=True)

# Single log file with date
LOG_FILE = LOGS_DIR / f"doit-{datetime.now().strftime('%Y-%m-%d')}.log"

# Create logger
logger = logging.getLogger("DOIT")
logger.setLevel(logging.DEBUG)

# File handler - writes to single file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)

# Console handler - also prints to terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Format with timestamp, level, and message
log_format = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(log_format)
console_handler.setFormatter(log_format)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Easy-to-use logging functions
def log_info(message: str, **kwargs):
    """Log info level"""
    extra = f" | {kwargs}" if kwargs else ""
    logger.info(f"{message}{extra}")


def log_error(message: str, error=None, **kwargs):
    """Log error level"""
    extra = f" | {kwargs}" if kwargs else ""
    error_msg = f" | Error: {error}" if error else ""
    logger.error(f"{message}{error_msg}{extra}")


def log_warning(message: str, **kwargs):
    """Log warning level"""
    extra = f" | {kwargs}" if kwargs else ""
    logger.warning(f"{message}{extra}")


def log_debug(message: str, **kwargs):
    """Log debug level"""
    extra = f" | {kwargs}" if kwargs else ""
    logger.debug(f"{message}{extra}")


def log_request(method: str, endpoint: str, user_id: str = None, **kwargs):
    """Log API request"""
    extra = f" | {kwargs}" if kwargs else ""
    user_info = f" | user_id={user_id}" if user_id else ""
    log_info(f"REQUEST | {method} {endpoint}{user_info}{extra}")


def log_response(status_code: int, endpoint: str, **kwargs):
    """Log API response"""
    extra = f" | {kwargs}" if kwargs else ""
    log_info(f"RESPONSE | {status_code} {endpoint}{extra}")


def log_database_operation(operation: str, table: str, **kwargs):
    """Log database operation"""
    extra = f" | {kwargs}" if kwargs else ""
    log_debug(f"DB | {operation} {table}{extra}")


def log_ai_call(ai_type: str, input_text: str, **kwargs):
    """Log AI API call"""
    extra = f" | {kwargs}" if kwargs else ""
    log_info(f"AI | {ai_type} | Input: {input_text[:50]}...{extra}")


def get_log_file_path():
    """Get current log file path"""
    return str(LOG_FILE)


def get_log_file_size():
    """Get size of log file in MB"""
    if LOG_FILE.exists():
        return LOG_FILE.stat().st_size / (1024 * 1024)
    return 0


print(f"\n📝 Logging initialized | File: {LOG_FILE}\n")

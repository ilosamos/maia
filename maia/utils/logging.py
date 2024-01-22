import logging

LOG_COLORS = {
    'DEBUG': '\033[94m',    # Blue
    'INFO': '\033[94m',     # Blue
    'WARNING': '\033[93m',  # Yellow
    'ERROR': '\033[91m',    # Red
    'CRITICAL': '\033[91m', # Red
    'ENDC': '\033[0m'       # End color
}

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, LOG_COLORS['ENDC'])
        message = super().format(record)
        return f"{log_color}{message}{LOG_COLORS['ENDC']}"
    
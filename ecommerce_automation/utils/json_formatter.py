"""JSON formatter for logging."""
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        if hasattr(record, 'test_id'):
            log_obj['test_id'] = record.test_id
            
        if hasattr(record, 'browser'):
            log_obj['browser'] = record.browser
            
        if hasattr(record, 'duration'):
            log_obj['duration'] = record.duration

        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_obj)

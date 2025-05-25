import logging
import logging.config
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

class TestLogger:
    """Centralized logging system for the test automation framework"""
    
    def __init__(self):
        self._setup_logging()
        self.test_logger = logging.getLogger('test_execution')
        self.db_logger = logging.getLogger('database')
        self.report_logger = logging.getLogger('reporting')
        self.pipeline_logger = logging.getLogger('pipeline')

    def _setup_logging(self):
        """Initialize logging configuration"""
        config_path = Path(__file__).parent.parent / 'config' / 'logging.yaml'
        
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
                },
                'json': {
                    'format': "%(asctime)s %(levelname)s %(name)s %(message)s",
                    '()': 'utils.logger.JsonFormatter'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'stream': 'ext://sys.stdout'
                },
                'test_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'json',
                    'filename': 'logs/test_execution/test.log',
                    'maxBytes': 10485760,
                    'backupCount': 5,
                    'encoding': 'utf8'
                }
            },
            'loggers': {
                'test_execution': {
                    'level': 'DEBUG',
                    'handlers': ['console', 'test_file'],
                    'propagate': False
                }
            },
            'root': {
                'level': 'INFO',
                'handlers': ['console']
            }
        }
        logging.config.dictConfig(config)

    def log_test_start(self, test_name, browser, **kwargs):
        """Log test execution start"""
        self.test_logger.info(
            f"Starting test: {test_name}",
            extra={
                'test_id': kwargs.get('test_id'),
                'browser': browser,
                'environment': kwargs.get('environment', 'test')
            }
        )

    def log_test_end(self, test_name, duration, status, **kwargs):
        """Log test execution end"""
        self.test_logger.info(
            f"Test completed: {test_name} - Status: {status}",
            extra={
                'test_id': kwargs.get('test_id'),
                'duration': duration,
                'status': status
            }
        )

    def log_test_step(self, step_name, status, **kwargs):
        """Log individual test step"""
        self.test_logger.debug(
            f"Test step: {step_name} - {status}",
            extra={
                'test_id': kwargs.get('test_id'),
                'step_name': step_name,
                'status': status
            }
        )

    def log_db_operation(self, operation, status, **kwargs):
        """Log database operations"""
        self.db_logger.debug(
            f"Database operation: {operation} - {status}",
            extra={
                'operation': operation,
                'status': status,
                'details': kwargs
            }
        )

    def log_report_generation(self, report_type, status, **kwargs):
        """Log report generation events"""
        self.report_logger.info(
            f"Report generation: {report_type} - {status}",
            extra={
                'report_type': report_type,
                'status': status,
                'details': kwargs
            }
        )

    def log_pipeline_event(self, event_type, status, **kwargs):
        """Log CI/CD pipeline events"""
        self.pipeline_logger.info(
            f"Pipeline event: {event_type} - {status}",
            extra={
                'event_type': event_type,
                'status': status,
                'details': kwargs
            }
        )

# Global logger instance
logger = TestLogger()

import logging
from logging.config import dictConfig
class SafeFormatter(logging.Formatter):
    def format(self,record):
        if not hasattr(record,"url"):
            record.url="_"
        if not hasattr(record,"method"):
            record.method="_"
        if not hasattr(record,"process_time"):
            record.process_time="_"
        if not hasattr(record,"status_code"):
            record.status_code="_"
        
        return super().format(record)
def setup_logging():
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
    
            "json": {
                "()":"core.logging.SafeFormatter",
                "format": ('"timestamp": "%(asctime)s",'
                ' "name": "%(name)s",'
                ' "level": "%(levelname)s",'
                ' "message": "%(message)s",'
                ' "method": "%(method)s",'
                ' "url": "%(url)s",'
                ' "process_time": "%(process_time)s",'
                ' "status_code": "%(status_code)s"}'),
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "formatter": "json",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    }
    dictConfig(logging_config)  
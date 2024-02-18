from .config_data import FOLDER_LOG

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename": FOLDER_LOG,
            "mode": "a",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "main": {
            "level": "DEBUG",
            "handlers": ["file"],
        },
        "sender": {
            "level": "DEBUG",
            "handlers": ["file"],
        },
        "DBworker": {
            "level": "DEBUG",
            "handlers": ["file"],
        }
    }
}

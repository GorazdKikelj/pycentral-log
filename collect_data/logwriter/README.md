### Setup logging

Logging setup was inspired by [mCoding YouTube channel](https://www.youtube.com/@mCoding). [Source code for this video](https://github.com/mCodingLLC/VideosSampleCode/tree/master/videos/135_modern_logging)


Default logging settings are stored in logconfig.json

Default setup file location C_LOG_DIR can be modified in logwriter\config.py.

Debug level can be adjusted with --debug_level directive from command line.
Command line directive --debug_level adjust sysout and file debug levels.

Logging configuration file logconfig.json
```
{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "simple": {
            "format": "%(levelname)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s|%(module)s|L%(lineno)d] : %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "pycentral-log.log",
            "maxBytes": 100000,
            "backupCount": 3
        }
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": [
                "stdout",
                "file"
            ]
        }
    }
}
```
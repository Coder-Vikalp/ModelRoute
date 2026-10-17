
import json
import logging
import os
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "schema_version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event_type": getattr(
                record, "event_type", "application_event"
            ),
            "message": record.getMessage(),
        }

        request_id = getattr(record, "request_id", None)
        if request_id is not None:
            log_entry["request_id"] = request_id

        error_code = getattr(record, "error_code", None)
        if error_code is not None:
            log_entry["error_code"] = error_code

        return json.dumps(log_entry)


def configure_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(
        os.getenv("LOG_LEVEL", "INFO").upper()
    )

    root_logger.handlers.clear()
    root_logger.addHandler(handler)


logger = logging.getLogger("modelroute")

from core.context import request_id
import logging

class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.requestid = request_id.get()
        return True
from uuid import uuid4
from core.context import request_id
import time
import logging

logger = logging.getLogger(__name__)

class CorrelationIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        token = request_id.set(str(uuid4()))
        response = self.get_response(request)
        response.headers['X-Request-ID'] = request_id.get()
        request_id.reset(token)
        return response
    
    
class RquestInfoMiddleware:
    def __init__(self, get_response):
          self.get_response = get_response
          
        
    def __call__(self, request):
        try:
            start = time.monotonic()
            response = self.get_response(request)
            duration = time.monotonic()-start
            if duration>3:
                logger.warning(f"{request.path} {request.method} {response.status_code} {duration}")
            else:
                logger.info(f"{request.path} {request.method} {response.status_code} {duration}")      
            return response
        except Exception:
            logger.exception("Error orccured")
            raise
            
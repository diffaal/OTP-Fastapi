from datetime import datetime
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class AppMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        exclude_paths = ["/health", "/available-threads"]

        if request.url.path in exclude_paths:
            response = await call_next(request)
        else:
            start_service = datetime.now()
            log_id = start_service.strftime("%y%m%d%H%M%S%f")
            request.state.log_id = log_id
            
            response = await call_next(request)
            
            service_process_time = datetime.now() - start_service
            logger.info(f"{log_id} - Time elapsed: {str(service_process_time.total_seconds() * 1000)}ms")

        return response

def get_log_id(request: Request):
    return request.state.log_id

import uvicorn
from anyio import to_thread
from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import APP_CONFIG
from exceptions.app_exception import OTPFastApiException
from exceptions.error_handler import app_error_handler, base_exception_handler
from middlewares.app_middleware import AppMiddleware
from models import engine
from routes.otp import otp_router
from routes.thread import thread_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    to_thread.current_default_thread_limiter().total_tokens = APP_CONFIG.THREAD_SIZE
    yield
    engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(title='OTP FASTAPI', lifespan=lifespan, debug=False)
    app.include_router(otp_router, prefix="/api/v1/otp")
    app.include_router(thread_router)
    app.add_exception_handler(OTPFastApiException, app_error_handler)
    app.add_exception_handler(Exception, base_exception_handler)
    app.add_middleware(AppMiddleware)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("__main__:app", host=APP_CONFIG.HOST, port=APP_CONFIG.PORT, workers=APP_CONFIG.SERVICE_WORKERS)

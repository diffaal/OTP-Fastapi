import uvicorn
from fastapi import FastAPI

from config import APP_CONFIG
from exceptions.app_exception import OTPFastApiException
from exceptions.error_handler import app_error_handler, base_exception_handler
from middlewares.app_middleware import AppMiddleware
from routes.otp import otp_router

def create_app() -> FastAPI:
    app = FastAPI(title='OTP FASTAPI', debug=False)
    app.include_router(otp_router)
    app.add_exception_handler(OTPFastApiException, app_error_handler)
    app.add_exception_handler(Exception, base_exception_handler)
    app.add_middleware(AppMiddleware)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("__main__:app", host=APP_CONFIG.HOST, port=APP_CONFIG.PORT, workers=APP_CONFIG.SERVICE_WORKERS)

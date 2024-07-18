from fastapi import Request
from fastapi.responses import JSONResponse
from http import HTTPStatus

from exceptions.app_exception import OTPFastApiException, exception_error_logger
from models.enums import ResponseMessage
from schemas.base_response import BaseResponse

def app_error_handler(request: Request, e: OTPFastApiException):
    return e.process_error_response()

def base_exception_handler(request: Request, e: Exception):
    exception_error_logger(e)
    res_body = BaseResponse(
        code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message=ResponseMessage.INTERNAL_SERVER_ERROR.value,
        data=dict()
    )
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=res_body.model_dump()
    )

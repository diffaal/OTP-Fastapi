from fastapi import Request
from fastapi.responses import JSONResponse
from http import HTTPStatus

from exceptions.app_exception import OTPFastApiException, error_logger
from models.enums import ResponseMessage
from schemas.base_response import BaseResponse

def app_error_handler(request: Request, e: OTPFastApiException):
    return e.process_error_response()

def base_exception_handler(request: Request, e: Exception):
    error_logger(e)
    res_body = BaseResponse(
        code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message=ResponseMessage.INTERNAL_SERVER_ERROR.value,
        data=dict()
    )
    return JSONResponse(content=res_body.model_dump())

from http import HTTPStatus
from traceback import format_exc
from loguru import logger

from models.enums import ResponseMessage
from helpers.response import make_base_response

class OTPFastApiException(Exception):
    def __init__(self, code, message, data) -> None:
        self.code = code
        self.message = message
        self.data = data
    
    def process_error_response(self):
        logger.error(f"Response exc type::{type(self).__name__}")
        response = make_base_response(self.code, self.message, self.data)
        logger.error(f"Response exc detail:: {response.body}")
        return response
        

class BadRequestException(OTPFastApiException):
    def __init__(self, message, data) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST, message, data)

class NotFoundException(OTPFastApiException):
    def __init__(self, message, data) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, message, data)

class UnauthorizedException(OTPFastApiException):
    def __init__(self, message, data) -> None:
        super().__init__(HTTPStatus.UNAUTHORIZED, message, data)

class InvalidRequestException(OTPFastApiException):
    def __init__(self, message, data) -> None:
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY, message, data)

class InternalErrorException(OTPFastApiException):
    def __init__(self, message, data) -> None:
        super().__init__(HTTPStatus.INTERNAL_SERVER_ERROR, message, data)

class DatabaseException(InternalErrorException):
    def __init__(self, data = None) -> None:
        super().__init__(ResponseMessage.DATABASE_ERROR.value, data)

def error_logger(e):
    logger.error(f"Exception Type::{type(e).__name__}")
    logger.error(f"Syserr::{e}")
    logger.error(f"Traceback::{format_exc()}")

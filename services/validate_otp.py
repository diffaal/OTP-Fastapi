from datetime import datetime
from http import HTTPStatus
from loguru import logger
from sqlalchemy.orm import Session

from exceptions.app_exception import BadRequestException
from helpers.otp_activity_validator import OTPActivityValidator
from models.enums import ActivityType, ResponseMessage
from repositories.otp_activity import OtpActivityRepository
from repositories.otp_list import OtpListRepository
from schemas.validate_otp import ValidateOTPRequest, ValidateOTPResponse, ValidateOTPResponseData

class ValidateOTPService:
    def __init__(self, db: Session, log_id) -> None:
        self.db = db
        self.otp_activity_repository = OtpActivityRepository(db)
        self.otp_list_repository = OtpListRepository(db)
        self.log_id = log_id

    def validate_otp(self, req: ValidateOTPRequest):
        phone_number = req.phone_number
        otp_code = req.otp_code

        otp_activity_validator = OTPActivityValidator(self.otp_activity_repository)
        val_otp_activity = otp_activity_validator.validate_otp_activity(phone_number, ActivityType.VALIDATE_OTP.value)

        err_message = self.validate_otp_code(phone_number, otp_code)
        if err_message:
            if not val_otp_activity.attempt:
                val_otp_activity.attempt = 1
            else:
                val_otp_activity.attempt += 1
            
            self.otp_activity_repository.update(val_otp_activity)
            
            res_data = ValidateOTPResponseData(
                validate_otp_failed_attempt=val_otp_activity.attempt
            ).model_dump()

            raise BadRequestException(err_message, res_data)
        
        res_data = ValidateOTPResponseData(
            validate_otp_failed_attempt=val_otp_activity.attempt
        )
        
        return ValidateOTPResponse(
            code=HTTPStatus.OK,
            message=ResponseMessage.SUCCESS.value,
            data=res_data.model_dump()
        ).model_dump()
        
    
    def validate_otp_code(self, phone_number, otp_code):
        otp_list = self.otp_list_repository.get_by_phone_number(phone_number)

        if not otp_list:
            raise BadRequestException(ResponseMessage.OTP_CODE_NOT_FOUND.value, None)

        now = datetime.now()
        if now > otp_list.expired_time:
            return ResponseMessage.OTP_EXPIRED.value
        
        if otp_list.is_used:
            return ResponseMessage.OTP_USED.value
        
        if otp_list.otp_code != otp_code:
            return ResponseMessage.INVALID_OTP.value
        
        otp_list.is_used = True
        self.otp_list_repository.update(otp_list)

        return None

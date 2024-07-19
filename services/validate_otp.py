from datetime import datetime
from fastapi.concurrency import run_in_threadpool
from http import HTTPStatus
from sqlalchemy.orm import Session

from exceptions.app_exception import BadRequestException
from helpers.otp_activity import OTPActivityHelper
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

    async def validate_otp(self, req: ValidateOTPRequest):
        otp_activity_helper = OTPActivityHelper(self.otp_activity_repository)

        val_otp_activity = await otp_activity_helper.validate_otp_activity(req.phone_number, ActivityType.VALIDATE_OTP.value)

        err_message = await self.validate_otp_code(req.phone_number, req.otp_code)
        if err_message:
            attempt = await otp_activity_helper.increment_activity_attempt(val_otp_activity)

            raise BadRequestException(
                err_message,
                ValidateOTPResponseData(
                    validate_otp_failed_attempt=attempt
                ).model_dump()
            )
        
        return ValidateOTPResponse(
            code=HTTPStatus.OK,
            message=ResponseMessage.SUCCESS.value,
            data=ValidateOTPResponseData(
                validate_otp_failed_attempt=val_otp_activity.attempt
            ).model_dump()
        ).model_dump()
        
    
    async def validate_otp_code(self, phone_number, otp_code):
        otp_list = await run_in_threadpool(
            self.otp_list_repository.get_by_phone_number,
            phone_number
        )

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
        await run_in_threadpool(
            self.otp_list_repository.update,
            otp_list
        )

        return None

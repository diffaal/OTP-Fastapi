from datetime import datetime, timedelta

from config import PARAM_CONFIG
from exceptions.app_exception import BadRequestException
from models.enums import ActivityType, ResponseMessage
from models.otp_activity import OtpActivity
from repositories.otp_activity import OtpActivityRepository
from schemas.generate_otp import GenerateOTPResponseData
from schemas.validate_otp import ValidateOTPResponseData


class OTPActivityValidator:
    def __init__(self, otp_activity_repository: OtpActivityRepository) -> None:
        self.otp_activity_repository = otp_activity_repository

    def validate_otp_activity(
        self,
        phone_number, 
        activity_type
    ):
        otp_activity = self.otp_activity_repository.get_last_otp_activity(phone_number, activity_type)
        
        if otp_activity:
            now = datetime.now()
            diff_hours = now - otp_activity.updated_at

            if activity_type == ActivityType.GENERATE_OTP.value:
                limit = PARAM_CONFIG.OTP_REQ_LIMIT
                cooldown_time = timedelta(hours=PARAM_CONFIG.OTP_REQ_COOLDOWN_HOURS)
            else:
                limit = PARAM_CONFIG.OTP_VALIDATE_LIMIT
                cooldown_time = timedelta(hours=PARAM_CONFIG.OTP_VALIDATE_COOLDOWN_HOURS)

            if diff_hours <= cooldown_time:
                if otp_activity.attempt >= limit:
                    if activity_type == ActivityType.GENERATE_OTP.value:
                        message = ResponseMessage.TOO_MANY_GENERATE_OTP.value
                        resp_data = GenerateOTPResponseData(generate_otp_attempt=otp_activity.attempt).model_dump()
                    else:
                        message = ResponseMessage.TOO_MANY_FAILED_VALIDATE_OTP.value
                        resp_data = ValidateOTPResponseData(validate_otp_failed_attempt=otp_activity.attempt).model_dump()
                    
                    raise BadRequestException(message, resp_data)
            else:
                otp_activity.attempt = 0
        else:
            new_otp_activity = OtpActivity(
                phone_number=phone_number,
                activity_type=activity_type,
                attempt=0
            )
            otp_activity = self.otp_activity_repository.add(new_otp_activity)
        
        return otp_activity
        
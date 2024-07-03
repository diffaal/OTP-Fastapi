from pydantic import BaseModel, field_validator

from config import PARAM_CONFIG
from schemas.base_response import BaseResponse


class ValidateOTPRequest(BaseModel):
    phone_number: str
    otp_code: str

    @field_validator("otp_code")
    def validate_otp_code_len(cls, value):
        if len(value) != PARAM_CONFIG.OTP_LENGTH:
            raise ValueError(f"otp_code must be {PARAM_CONFIG.OTP_LENGTH} characters")
        return value
    
    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        return value.strip()


class ValidateOTPResponseData(BaseModel):
    validate_otp_failed_attempt: int
class ValidateOTPResponse(BaseResponse):
    data: ValidateOTPResponseData

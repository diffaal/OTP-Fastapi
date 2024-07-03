from pydantic import BaseModel, field_validator, model_validator

from models.country_code import country_code_db
from models.enums import OTPSender
from schemas.base_response import BaseResponse

otp_senders = [otp_sender.value for otp_sender in OTPSender]

class GenerateOTPRequest(BaseModel):
    phone_number: str
    country_code: str
    otp_sender: str
    
    @field_validator("otp_sender")
    def validate_otp_sender_value(cls, value):
        value = value.strip().upper()
        if value not in otp_senders:
            raise ValueError("Invalid otp sender")
        return value
    
    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        return value.strip()
    
    @field_validator("country_code")
    def validate_country_code(cls, value):
        value = value.strip()
        if value != "62":
            country_code_check = "+" + value
            if not any(
                code.get("code") == country_code_check
                for code in country_code_db
            ):
                raise ValueError("Invalid country code")
        return value
    
    @model_validator(mode="after")
    def validate_phone_country(self):
        len_country_code = len(self.country_code)
        if self.phone_number[:len_country_code] != self.country_code:
            raise ValueError("phone_number and country_code not match")
        return self

class GenerateOTPResponseData(BaseModel):
    generate_otp_attempt: int
class GenerateOTPResponse(BaseResponse):
    data: GenerateOTPResponseData

from enum import Enum

class ResponseMessage(Enum):
    SUCCESS = "Success"
    INTERNAL_SERVER_ERROR = "Internal server error"
    DATABASE_ERROR = "Database error"
    TOO_MANY_GENERATE_OTP = "Too many generate OTP"
    TOO_MANY_FAILED_VALIDATE_OTP = "Too many failed validate OTP"
    OTP_CODE_NOT_FOUND = "OTP code not found, must OTP request first"
    OTP_EXPIRED = "OTP code has been expired"
    OTP_USED = "OTP code has been used"
    INVALID_OTP = "Invalid OTP code"
    WA_SENDER_CONNECTION_ERROR = "Connection error to WA Sender"
    WA_SENDER_TIMEOUT = "Connection timeout to WA Sender"
    WA_SENDER_RESPONSE_NOT_OK = "Not ok response status code from WA Sender"
    OTP_BEING_PROCESSED = "OTP is being processed"

class ActivityType(Enum):
    GENERATE_OTP = "GENERATE_OTP"
    VALIDATE_OTP = "VALIDATE_OTP"

class OTPSender(Enum):
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"

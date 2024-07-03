import secrets
import string

from config import PARAM_CONFIG

class OTPCodeGenerator:
    def generate_otp_code():
        otp_code = ""
        digits = string.digits
        for _ in range(PARAM_CONFIG.OTP_LENGTH):
            otp_code += str(secrets.choice(digits))
        
        return otp_code

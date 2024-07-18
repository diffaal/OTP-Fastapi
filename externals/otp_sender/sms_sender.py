from externals.otp_sender import OTPSender

class SMSSender(OTPSender):
    async def send_otp(self, phone_number, otp_code, log_id):
        pass
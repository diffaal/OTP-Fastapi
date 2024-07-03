from abc import ABC, abstractmethod

class OTPSender(ABC):
    @abstractmethod
    def send_otp(self, phone_number, otp_code, log_id):
        pass
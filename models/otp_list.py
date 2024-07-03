from sqlalchemy import Column, String, Boolean, DateTime

from models.base_model import BaseModel

class OtpList(BaseModel):
    __tablename__ = "otp_list"

    phone_number = Column(String(20))
    otp_code = Column(String(20))
    expired_time = Column(DateTime)
    is_used = Column(Boolean)

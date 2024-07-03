from sqlalchemy import Column, String, Integer

from models.base_model import BaseModel

class OtpActivity(BaseModel):
    __tablename__ = "otp_activity"

    phone_number = Column(String(20))
    activity_type = Column(String(20))
    attempt = Column(Integer)

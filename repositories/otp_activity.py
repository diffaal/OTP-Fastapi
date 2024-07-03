from sqlalchemy.orm import Session

from exceptions.app_exception import error_logger
from exceptions.app_exception import DatabaseException
from models.otp_activity import OtpActivity

class OtpActivityRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def add(self, new_otp_activity: OtpActivity):
        try:
            self.db.add(new_otp_activity)
            self.db.commit()
            self.db.refresh(new_otp_activity)
            return new_otp_activity
        except Exception as e:
            self.db.rollback()
            error_logger(e)
            raise DatabaseException()

    def update(self, otp_activity: OtpActivity):
        try:
            self.db.add(otp_activity)
            self.db.commit()
            self.db.refresh(otp_activity)
            return otp_activity
        except Exception as e:
            self.db.rollback()
            error_logger(e)
            raise DatabaseException()
    
    def get_last_otp_activity(self, phone_number, activity_type):
        try:
            return self.db.query(OtpActivity).filter(
                OtpActivity.phone_number == phone_number,
                OtpActivity.activity_type == activity_type
            ).order_by(OtpActivity.updated_at.desc()).first()
        except Exception as e:
            self.db.rollback()
            error_logger(e)
            raise DatabaseException()

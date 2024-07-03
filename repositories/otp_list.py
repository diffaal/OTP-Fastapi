from sqlalchemy.orm import Session

from exceptions.app_exception import error_logger
from exceptions.app_exception import DatabaseException
from models.otp_list import OtpList

class OtpListRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def add(self, new_otp_list: OtpList):
        try:
            self.db.add(new_otp_list)
            self.db.commit()
            self.db.refresh(new_otp_list)
            return new_otp_list
        except Exception as e:
            self.db.rollback()
            error_logger(e)
            raise DatabaseException()
    
    def update(self, otp_list: OtpList):
        try:
            self.db.add(otp_list)
            self.db.commit()
            self.db.refresh(otp_list)
            return otp_list
        except Exception as e:
            self.db.rollback()
            error_logger(e)
            raise DatabaseException()
    
    def get_by_phone_number(self, phone_number):
        try:
            return self.db.query(OtpList).filter(OtpList.phone_number == phone_number).first()
        except Exception as e:
            self.db.rollback()
            error_logger(e)
            raise DatabaseException()

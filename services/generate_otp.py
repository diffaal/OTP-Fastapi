from datetime import datetime, timedelta
from fastapi.concurrency import run_in_threadpool
from http import HTTPStatus
from loguru import logger
from sqlalchemy.orm import Session

from config import PARAM_CONFIG
from externals.otp_sender.wa_sender import WASender
from externals.otp_sender.sms_sender import SMSSender
from helpers.otp_activity_validator import OTPActivityValidator
from helpers.otp_code_generator import OTPCodeGenerator
from models.enums import ActivityType, OTPSender, ResponseMessage
from models.otp_list import OtpList
from repositories.otp_activity import OtpActivityRepository
from repositories.otp_list import OtpListRepository
from schemas.generate_otp import GenerateOTPRequest, GenerateOTPResponse, GenerateOTPResponseData


class GenerateOTPService:
    def __init__(self, db: Session, log_id) -> None:
        self.otp_activity_repository = OtpActivityRepository(db)
        self.otp_list_repository = OtpListRepository(db)
        self.log_id = log_id

    async def generate_otp(self, req: GenerateOTPRequest):
        phone_number = req.phone_number
        otp_sender = req.otp_sender
        
        otp_activity_validator = OTPActivityValidator(self.otp_activity_repository)
        gen_otp_activity = await otp_activity_validator.validate_otp_activity(phone_number, ActivityType.GENERATE_OTP.value)
        _ = await otp_activity_validator.validate_otp_activity(phone_number, ActivityType.VALIDATE_OTP.value)
        
        otp_code = OTPCodeGenerator.generate_otp_code()
        logger.info(f"OTP Code : {otp_code}")

        if otp_sender == OTPSender.WHATSAPP.value:
            otp_sender_service = WASender()
        elif otp_sender == OTPSender.SMS.value:
            otp_sender_service = SMSSender()
        
        start_sm = datetime.now()
        logger.info(f'{self.log_id} - Send OTP Message process started')

        await otp_sender_service.send_otp(phone_number, otp_code, self.log_id)

        end_sm = datetime.now()
        sm_time = end_sm - start_sm
        logger.info(f"{self.log_id} - Send OTP Message finished. Time elapsed: {sm_time.total_seconds() * 1000}ms")
        
        await self.insert_otp_code(phone_number, otp_code)

        if not gen_otp_activity.attempt:
            gen_otp_activity.attempt = 1
        else:
            gen_otp_activity.attempt += 1

        await run_in_threadpool(
            self.otp_activity_repository.update,
            gen_otp_activity
        )

        res_data = GenerateOTPResponseData(generate_otp_attempt=gen_otp_activity.attempt)

        return GenerateOTPResponse(
            code=HTTPStatus.OK,
            message=ResponseMessage.SUCCESS.value,
            data=res_data.model_dump()
        ).model_dump()
    
    async def insert_otp_code(self, phone_number, otp_code):
        now = datetime.now()
        expired_minute = timedelta(minutes=PARAM_CONFIG.OTP_CODE_EXPIRED_MINUTES)
        otp_expired = now + expired_minute

        otp_list = await run_in_threadpool(
            self.otp_list_repository.get_by_phone_number,
            phone_number
        )
        if otp_list:
            otp_list.otp_code = otp_code
            otp_list.is_used = False
            otp_list.expired_time = otp_expired

            await run_in_threadpool(
                self.otp_list_repository.update,
                otp_list
            )
        else:
            new_otp_list = OtpList(
                phone_number=phone_number,
                otp_code=otp_code,
                is_used=False,
                expired_time=otp_expired
            )
            await run_in_threadpool(
                self.otp_list_repository.add,
                new_otp_list
            )

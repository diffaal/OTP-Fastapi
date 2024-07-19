from datetime import datetime, timedelta
from fastapi.concurrency import run_in_threadpool
from http import HTTPStatus
from loguru import logger
from sqlalchemy.orm import Session

from config import PARAM_CONFIG
from externals.otp_sender.wa_sender import WASender
from externals.otp_sender.sms_sender import SMSSender
from helpers.otp_activity import OTPActivityHelper
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
        otp_activity_helper = OTPActivityHelper(self.otp_activity_repository)
    
        gen_otp_activity = await otp_activity_helper.validate_otp_activity(req.phone_number, ActivityType.GENERATE_OTP.value)
        _ = await otp_activity_helper.validate_otp_activity(req.phone_number, ActivityType.VALIDATE_OTP.value)
        
        otp_code = OTPCodeGenerator.generate_otp_code()
        logger.info(f"OTP Code : {otp_code}")

        await self.send_otp_code(req, otp_code)
        
        await self.insert_otp_code(req.phone_number, otp_code)

        attempt = await otp_activity_helper.increment_activity_attempt(gen_otp_activity)

        return GenerateOTPResponse(
            code=HTTPStatus.OK,
            message=ResponseMessage.SUCCESS.value,
            data=GenerateOTPResponseData(generate_otp_attempt=attempt).model_dump()
        ).model_dump()
    
    async def send_otp_code(self, req: GenerateOTPRequest, otp_code):
        if req.otp_sender == OTPSender.WHATSAPP.value:
            otp_sender_service = WASender()
        elif req.otp_sender == OTPSender.SMS.value:
            otp_sender_service = SMSSender()
        
        start_sm = datetime.now()
        logger.info(f'{self.log_id} - Send OTP Message process started')

        await otp_sender_service.send_otp(req.phone_number, otp_code, self.log_id)

        end_sm = datetime.now()
        sm_time = end_sm - start_sm
        logger.info(f"{self.log_id} - Send OTP Message finished. Time elapsed: {sm_time.total_seconds() * 1000}ms")

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

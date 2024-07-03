
import json
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

from middlewares.app_middleware import get_log_id
from models import get_db
from schemas.generate_otp import GenerateOTPRequest, GenerateOTPResponse
from schemas.validate_otp import ValidateOTPRequest, ValidateOTPResponse
from services.generate_otp import GenerateOTPService
from services.validate_otp import ValidateOTPService

otp_router = APIRouter()

@otp_router.post(
    "/generate",
    response_model=GenerateOTPResponse,
    response_model_exclude_unset=True, 
    tags=["Generate OTP"]
)
def generate_otp_route(req: GenerateOTPRequest, db: Session = Depends(get_db), log_id: str = Depends(get_log_id)):
    logger.info(f"{log_id} - Start to processing Generate OTP Service. Request:\n{json.dumps(dict(req), indent=2)}")

    result = GenerateOTPService(db, log_id).generate_otp(req)

    logger.info(f"{log_id} - Finished process Generate OTP Service. Response:\n{json.dumps(result, indent=2)}")
    return result

@otp_router.post(
    "/validate",
    response_model=ValidateOTPResponse,
    response_model_exclude_unset=True, 
    tags=["Validate OTP"]
)
def validate_otp_route(req: ValidateOTPRequest, db: Session = Depends(get_db), log_id: str = Depends(get_log_id)):
    logger.info(f"{log_id} - Start to processing Validate OTP Service. Request:\n{json.dumps(dict(req), indent=2)}")

    result = ValidateOTPService(db, log_id).validate_otp(req)

    logger.info(f"{log_id} - Finished process Validate OTP Service. Response:\n{json.dumps(result, indent=2)}")

    return result

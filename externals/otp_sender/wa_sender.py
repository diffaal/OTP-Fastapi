import httpx
import json
from loguru import logger

from config import PARAM_CONFIG
from exceptions.app_exception import InternalErrorException, exception_error_logger

from externals.otp_sender import OTPSender
from models.enums import ResponseMessage

class WASender(OTPSender):
    async def send_otp(self, phone_number, otp_code, log_id):
        req_body = {
            "channelId": "EFORM", 
            "partnerId": PARAM_CONFIG.WA_PROJECT_ID, 
            "projectType": PARAM_CONFIG.WA_TYPE, 
            "mobileNum": phone_number, 
            "param1": otp_code, 
            "param2": "", 
            "param3": "",
            "jenis_rekening": ""
        }

        logger.info(f"Whatsapp Gateway Send Message URL: {PARAM_CONFIG.WA_SENDER_URL}")
        logger.info(f"Whatsapp Gateway Send Message Request Body:\n{json.dumps(req_body, indent=2)}")

        try:
            res_body = None
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    PARAM_CONFIG.WA_SENDER_URL,
                    json=req_body,
                )
                status_code = response.status_code
                logger.info(f"Whatsapp Gateway Send Message Response Status Code: {status_code}")
                if status_code != 200:
                    logger.info(f"Whatsapp Gateway Send Message Response Body:\n{response.text}")
                    raise InternalErrorException(ResponseMessage.WA_SENDER_RESPONSE_NOT_OK.value)
                
                res_body = response.json()
                logger.info(f"Whatsapp Gateway Send Message Response Body:\n{json.dumps(res_body, indent=2)}")
        except httpx.NetworkError as e:
            exception_error_logger(e)
            raise InternalErrorException(ResponseMessage.WA_SENDER_CONNECTION_ERROR.value)
        except httpx.TimeoutException as e:
            exception_error_logger(e)
            raise InternalErrorException(ResponseMessage.WA_SENDER_TIMEOUT.value)

        error_code = res_body.get("errorCode", "")
        error_message = res_body.get("errorMessage", "")
        if error_code != "200":
            logger.error(f"WA Sender:: {error_message}")
            raise InternalErrorException(f"WA Sender:: {error_message}")

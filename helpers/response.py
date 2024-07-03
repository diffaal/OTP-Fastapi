from fastapi.responses import JSONResponse

from schemas.base_response import BaseResponse

def make_base_response(status_code, message , data):
    res_body = BaseResponse(
        code=status_code,
        message=message,
        data=data
    ).model_dump()
    return JSONResponse(status_code=status_code, content=res_body)

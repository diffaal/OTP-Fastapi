from pydantic import BaseModel
from typing import Optional

class BaseResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None

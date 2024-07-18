from anyio import to_thread
from fastapi import APIRouter

thread_router = APIRouter()

@thread_router.get(
    "/available-threads",
    tags=["Get Available Threads"]
)
async def thread_route():
    return to_thread.current_default_thread_limiter().available_tokens

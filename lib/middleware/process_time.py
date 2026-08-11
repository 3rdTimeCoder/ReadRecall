import time
from fastapi import Request


async def add_process_time_header(request: Request, call_next):
    """Middleware that adds an X-Process-Time header to every response.

    Measures the time taken to process the request and includes it as a
    response header for observability.

    Args:
        request: The incoming FastAPI request.
        call_next: The next middleware or route handler in the chain.

    Returns:
        The response with the X-Process-Time header added.
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
from starlette.requests import Request
from starlette.responses import Response


async def logger_middleware(request: Request, call_next):
    """Middleware to log each request with its unique request ID."""
    request_id = getattr(request.state, "request_id", None)
    print(f"Request ID: {request_id} - Path: {request.url.path} - Method: {request.method}")
    response: Response = await call_next(request)
    print(f"Request ID: {request_id} - Response: {response.status_code}")
    return response

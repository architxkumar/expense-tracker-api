from starlette.requests import Request
from starlette.responses import Response

import uuid


async def request_id_middleware(request: Request, call_next):
    """Middleware to add a unique request ID to each request."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response: Response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

from starlette.requests import Request
from starlette.responses import Response, JSONResponse


async def error_handler_middleware(request: Request, call_next):
    """Middleware to handle errors and return standardized error responses."""
    try:
        response: Response = await call_next(request)
        return response
    except Exception as e:
        request_id = getattr(request.state, "request_id", None)
        print(f"Request ID: {request_id} - Error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "request_id": request_id},
        )

from starlette.responses import Response


async def cross_origin_resource_sharing_middleware(request, call_next):
    """CORS middleware with preflight handling."""
    if request.method == "OPTIONS":
        # Handle preflight early
        response: Response = Response(status_code=200)
    else:
        response: Response = await call_next(request)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response
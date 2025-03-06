from dataclasses import dataclass
from fastapi import Request
import json
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from utils import request_queue


@dataclass
class UserRateLimit:
    start_time: int
    request_count: int


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, request_limit: int, seconds: int):
        super().__init__(app)
        self.request_limit = request_limit
        self.seconds = seconds

    # def _get_client_id(self, request: Request) -> str:
    #     return f"{request.client.host}:{request.client.port}"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        body = await request.body()
        request_id = id(request)
        request_data = {
            "id": request_id,
            "type": request.scope.get("type"),
            "path": request.scope.get("path"),
            "method": request.scope.get("method"),
            "query_string": request.scope.get("query_string"),
            "headers": request.scope.get("headers"),
        }
        if body:
            request_data["body"] = json.loads(body)

        await request_queue.put(request_data)
        return await call_next(request)

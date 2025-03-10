from dataclasses import dataclass, field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import SERVER_HOST, SERVER_PORT
from middlewares.rate_limiter import RateLimiterMiddleware
from routes.backtest_router import BacktestRouter
from utils import app_lifespan


@dataclass
class HttpOptions:
    base_path: str = "/v1"
    allow_credentials: bool = True
    allow_origins: list[str] = field(default_factory=lambda: ["*"])
    allow_methods: list[str] = field(default_factory=lambda: ["*"])
    allow_headers: list[str] = field(default_factory=lambda: ["*"])


class HttpService:
    def __init__(
        self,
        host: str = SERVER_HOST,
        port: int = SERVER_PORT,
        options: HttpOptions = HttpOptions(),
    ):
        self.options = options
        self._host = host
        self._port = port
        self._app = FastAPI(root_path_in_servers=True, lifespan=app_lifespan)
        self._initialized = False

    def _init_app(self):
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=self.options.allow_origins,
            allow_credentials=self.options.allow_credentials,
            allow_methods=self.options.allow_methods,
            allow_headers=self.options.allow_headers,
        )
        self._app.add_middleware(RateLimiterMiddleware, request_limit=2, seconds=5)

    def _create_routes(self):
        """Add all of FastAPI routers"""
        self._app.include_router(
            BacktestRouter().route,
            prefix=self.options.base_path,
            tags=["Backtests API"],
        )

    def _init_server(self):
        if not self._initialized:
            self._init_app()
            self._create_routes()
            self._initialized = True

    def get_app(self):
        self._init_server()
        return self._app

    def start(self):
        self._init_server()
        uvicorn.run(self._app, host=self._host, port=self._port)

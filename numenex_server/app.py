from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import Config, get_settings
from .dependencies import (
    Database,
    DatabaseDependency,
    CommuneDependency,
    UniswapV3Dependency,
)
from .routers import trade_router, nonce_router
from .commune import VerifyCommuneMinersAndValis
from .graphql import UniswapV3Graphql
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from .middlewares.exception import ExceptionHandlerMiddleware


class App:
    app: FastAPI
    config: Config

    def __init__(self, config: Config):
        self.config = config
        dependencies = self.get_dependencies()
        self.app = FastAPI(dependencies=dependencies)
        self.include_routes()

    def get_dependencies(self):
        db = Database(self.config.database_config)
        database_dependency = DatabaseDependency(db)
        commune_verifier = VerifyCommuneMinersAndValis(self.config.commune_config)
        commune_dependency = CommuneDependency(commune_verifier)
        uniswap_v3_graphql = UniswapV3Graphql(self.config.uniswap_graphql_config)
        uniswap_v3_dependency = UniswapV3Dependency(uniswap_v3_graphql)
        return [
            Depends(database_dependency),
            Depends(commune_dependency),
            Depends(uniswap_v3_dependency),
        ]

    def include_routes(self):
        self.app.include_router(trade_router.router)
        self.app.include_router(nonce_router.router)


settings = get_settings()
app = App(settings)
app.app.add_middleware(
    SessionMiddleware, secret_key="some-random-string", max_age=180000
)
app.app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.app.add_middleware(ExceptionHandlerMiddleware)


def serve():
    uvicorn.run("numenex_server.app:app.app", host="0.0.0.0", port=8001, reload=True)

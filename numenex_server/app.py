from fastapi import Depends, FastAPI
from .settings import Config, get_settings
from .dependencies import Database, DatabaseDependency, CommuneDependency
from .routers import trade_router, nonce_router
from .commune import VerifyCommuneMinersAndValis
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
        return [Depends(database_dependency), Depends(commune_dependency)]

    def include_routes(self):
        self.app.include_router(trade_router.router)
        self.app.include_router(nonce_router.router)


settings = get_settings()
app = App(settings)
app.app.add_middleware(ExceptionHandlerMiddleware)
app.app.add_middleware(
    SessionMiddleware, secret_key="some-random-string", max_age=180000
)


def serve():
    uvicorn.run("numenex_server.app:app.app", host="0.0.0.0", port=8001, reload=True)

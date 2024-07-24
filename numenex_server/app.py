from fastapi import Depends, FastAPI
from .settings import Config, get_settings
from .dependencies import Database, DatabaseDependency
from .routers import trade_router
import uvicorn


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
        return [Depends(database_dependency)]

    def include_routes(self):
        self.app.include_router(trade_router.router)


settings = get_settings()
app = App(settings)


def serve():
    uvicorn.run("numenex_server.app:app.app", host="0.0.0.0", port=8001, reload=True)

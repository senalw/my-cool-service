import logging
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from settings import ROOT_DIR
from src.api.v1.routes import routers as v1_routers
from src.core.auth.auth_interceptor import AuthInterceptor
from src.core.container import Container
from src.core.exception import AuthenticationError, AuthorizationError
from src.util.singleton import singleton
from starlette.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@singleton
class AppCreator:
    def __init__(self) -> None:

        # set db and container
        self.container = Container()
        self.db = self.container.db()
        self.config = self.container.configs()
        self.auth_interceptor = AuthInterceptor(self.config.security_config)
        self.ssl_certificate = f"{ROOT_DIR}/certs/service/public.crt"
        self.ssl_private_key = f"{ROOT_DIR}/certs/service/private.key"

        # set app default
        self.app = FastAPI(
            title=self.config.app_config.name,
            openapi_url=f"{self.config.app_config.api}/openapi.json",
            version=self.config.app_config.version,
            swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        )

        # CORS middleware for handling cross-origin requests
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allow requests from any origin.
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["*"],
        )

        # BELOW SECTION ADDED FOR TESTING PURPOSE #
        # table creation can be done using flyway
        self.db.drop_tables()
        self.db.create_tables()

        # insert same data
        self.db.insert_sample_data()
        #######################################################

        # Route to serve the Swagger UI
        @self.app.get("/docs", include_in_schema=False)
        async def custom_swagger_ui_html() -> Any:
            return self.app.openapi_html()

        # Route to serve the OpenAPI schema
        @self.app.get("/openapi.json", include_in_schema=False)
        async def get_openapi() -> Dict[str, Any]:
            return self.app.openapi()

        @self.app.middleware("https")
        async def opa_authorization(request: Request, call_next: Any) -> Any:
            try:
                # Call the auth interceptor to handle OPA authorization
                await self.auth_interceptor.intercept(request)
            except (AuthenticationError, AuthorizationError) as e:
                return JSONResponse({"error": str(e)}, status_code=e.status_code)

            # Access granted, allow request to proceed to the endpoint
            response = await call_next(request)
            return response

        self.app.include_router(v1_routers, prefix="/api/v1")


if __name__ == "__main__":
    app_creator = AppCreator()
    app = app_creator.app
    conf = app_creator.config
    uvicorn.run(
        app,
        host="0.0.0.0",  # noqa S104
        port=conf.app_config.port,
        ssl_certfile=app_creator.ssl_certificate,
        ssl_keyfile=app_creator.ssl_private_key,
    )

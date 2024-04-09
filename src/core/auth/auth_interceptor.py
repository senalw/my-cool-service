import logging
import re
from typing import Optional

import requests
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from jose import ExpiredSignatureError, jwt
from jose.exceptions import JWTClaimsError, JWTError
from requests.exceptions import ConnectionError
from src.config.config import Config
from src.core.container import Container
from src.core.exception import AuthenticationError, AuthorizationError
from src.module.user import UserRepository
from starlette.requests import Request


class AuthInterceptor:
    def __init__(self, configs: Config.SecurityConfig) -> None:
        self.configs = configs

    async def intercept(self, request: Request) -> None:
        url_path = re.sub(str(request.base_url), "", str(request.url))
        match = re.search(
            r"api/[^/]+/users", url_path
        )  # do authorization only for the paths with "api/v*/user". # noqa E501
        if match:
            # Extract authentication token from request headers
            token = request.headers.get("Authorization")
            if not token:
                raise AuthenticationError("Authentication token is missing")

            self.authenticate_user(token)  # validate token

            # Construct request object for OPA
            request_data = {
                "input": {
                    "method": request.method,
                    "path": request.url.path,
                    "token": token,
                }
            }

            # Send request to OPA for policy evaluation
            opa_response = None
            try:
                opa_response = requests.post(self.configs.opa_url, json=request_data)
            except ConnectionError as e:
                logging.exception(e)

            if not opa_response or not opa_response.ok:
                raise AuthorizationError("OPA evaluation failed")

            # Check OPA decision
            decision = opa_response.json().get("result", {}).get("allow", False)

            if not decision:
                raise AuthorizationError("Access Denied")

    @inject
    def authenticate_user(
        self,
        token: str,
        user_repo: UserRepository = Depends(  # noqa B008
            Provide[Container.user_repository]
        ),
    ) -> None:
        try:
            decoded_token = jwt.decode(
                token=token.split()[1],  # remove "Bearer" prefix from the token
                key=self.configs.secret_key,
                algorithms=self.configs.algorithm,
            )
            # Check whether the user is actually exists in the database to stop accessibility of deleted users during token validation period. # noqa E501
            username: Optional[str] = decoded_token.get("username", None)
            if not user_repo.get_user_by_id(username):
                raise AuthenticationError(f"Unable to access for the user {username}")
        except (JWTError, ExpiredSignatureError, JWTClaimsError):
            raise AuthenticationError("JWT token authentication failed")

import logging
import re
from typing import Optional

import requests
import urllib3
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from jose import ExpiredSignatureError, jwt
from jose.exceptions import JWTClaimsError, JWTError
from requests.exceptions import ConnectionError
from settings import ROOT_DIR
from src.config.config import Config
from src.core.container import Container
from src.core.exception import AuthenticationError, AuthorizationError
from src.module.user import UserRepository
from src.util.utils import is_self_signed
from starlette.requests import Request
from urllib3.exceptions import InsecureRequestWarning


class AuthInterceptor:
    def __init__(self, configs: Config.SecurityConfig) -> None:
        self.configs = configs
        # Generate self-signed certificates
        # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout private.key -out public.crt -subj "/CN=localhost" -addext "subjectAltName = DNS:localhost" # noqa E501
        # If certificates are ca signed certificates, then verify=f"{ROOT_DIR}/{self.configs.opa_public_key}", otherwise it should be "verify=False".  # noqa E501
        if is_self_signed(self.__read_certificate()):
            self.verify = False
            urllib3.disable_warnings(InsecureRequestWarning)
        else:
            self.verify = f"{ROOT_DIR}/{self.configs.opa_public_key}"

    async def intercept(self, request: Request) -> None:
        match = re.search(r"api/[^/]+/users", request.url.path)
        if match:  # do authorization only for the paths with "api/v*/user". # noqa E501
            # Extract authentication token from request headers
            token = request.headers.get("Authorization")
            if not token:
                raise AuthenticationError("Authentication token is missing")

            match = re.match(r"^Bearer\s+(.*)$", token)
            token = (
                match.group(1)  # remove "Bearer" prefix from the token if exists.
                if match
                else token
            )

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
                opa_response = requests.post(
                    self.configs.opa_url,
                    json=request_data,
                    verify=self.verify,
                )
            except ConnectionError as e:
                logging.exception(e)

            if not opa_response or not opa_response.ok:
                raise AuthorizationError("OPA evaluation failed")

            # Check OPA decision
            decision = opa_response.json().get("result", {}).get("allow", False)

            if not decision:
                logging.error(f"{request.method} request is unauthorized")
                raise AuthorizationError("Access Denied")
            logging.info(f"{request.method} request is authorized")

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
                token=token,
                key=self.configs.secret_key,
                algorithms=self.configs.algorithm,
            )
            # Check whether the user is actually exists in the database to stop accessibility of deleted users during token validation period. # noqa E501
            username: Optional[str] = decoded_token.get("username", None)
            if not user_repo.get_user_by_id(username):
                raise AuthenticationError(f"Unable to access for the user {username}")
        except (JWTError, ExpiredSignatureError, JWTClaimsError) as e:
            logging.exception("JWT token authentication failed", e)
            raise AuthenticationError("JWT token authentication failed")

    def __read_certificate(self) -> bytes:
        with open(f"{ROOT_DIR}/{self.configs.opa_public_key}", "rb") as cert_file:
            cert_data = cert_file.read()
        return cert_data

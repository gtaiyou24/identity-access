import json

import requests
from di import DIContainer
from fastapi import APIRouter, Depends

from application.identity import IdentityApplicationService
from application.identity.command import AuthenticateProviderUserCommand
from port.adapter.resource.auth.github.request import AccessTokenRequest
from port.adapter.resource.auth.response import Token


class GitHubResource:
    router = APIRouter(prefix='/auth/github', tags=['Auth'])
    GITHUB_API = 'https://api.github.com'

    def __init__(self, client_id: str, client_secret: str):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.router.add_api_route("/token", self.token, methods=["POST"], response_model=Token)

    def token(self, request: AccessTokenRequest = Depends()) -> Token:
        application_service = DIContainer.instance().resolve(IdentityApplicationService)

        headers = {'Authorization': f"Bearer {self.__access_token_from(request.code)}"}
        user = requests.get(f'{self.GITHUB_API}/user', headers=headers).json()
        emails = requests.get(f'{self.GITHUB_API}/user/emails', headers=headers).json()

        command = AuthenticateProviderUserCommand.github(user, emails)
        dpo = application_service.authenticate_provider_user(command)
        return Token.generate(dpo)

    def __access_token_from(self, code: str) -> str:
        access_token = requests.post(
            'https://github.com/login/oauth/access_token',
            headers={'Accept': 'application/json'},
            params={'client_id': self.__client_id, 'client_secret': self.__client_secret, 'code': code}
        ).json()
        return access_token['access_token']


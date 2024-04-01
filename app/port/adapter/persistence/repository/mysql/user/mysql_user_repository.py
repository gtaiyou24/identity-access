from __future__ import annotations

from injector import inject

from domain.model.user import UserRepository, EmailAddress, User
from port.adapter.persistence.repository.mysql.user import CacheLayerUser


class MySQLUserRepository(UserRepository):
    @inject
    def __init__(self, cache_layer_user: CacheLayerUser):
        self.__cache_layer_user = cache_layer_user

    def add(self, user: User) -> None:
        self.__cache_layer_user.set(user)

    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        return self.__cache_layer_user.user_or_origin(email_address)

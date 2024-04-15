from __future__ import annotations

import abc

from domain.model.token import Token


class TokenRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, value: str) -> Token | None:
        pass

    @abc.abstractmethod
    def add(self, token: Token) -> None:
        pass

    @abc.abstractmethod
    def remove(self, token: Token) -> None:
        pass

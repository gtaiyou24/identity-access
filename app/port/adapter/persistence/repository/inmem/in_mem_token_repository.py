from __future__ import annotations

from domain.model.token import TokenRepository, Token


class InMemTokenRepository(TokenRepository):
    tokens: set[Token] = set()

    def get(self, value: str) -> Token | None:
        for e in self.tokens:
            if e.value == value:
                return e
        return None

    def add(self, token: Token) -> None:
        self.tokens.add(token)

    def remove(self, token: Token) -> None:
        self.tokens.remove(token)

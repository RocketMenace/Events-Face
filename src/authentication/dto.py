from dataclasses import dataclass

from rest_framework.fields import UUIDField


@dataclass(kw_only=True)
class UserDTO:
    username: str
    password: str | None = None
    id: UUIDField | None = None


@dataclass(kw_only=True, frozen=True, eq=False)
class TokensDTO:
    access: str | None = None
    refresh: str | None = None


@dataclass(kw_only=True, frozen=True, eq=False)
class UserCredentialsDTO:
    username: str
    password: str

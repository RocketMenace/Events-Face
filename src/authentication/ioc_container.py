from functools import lru_cache

import punq

from src.authentication.repository import UserRepository
from src.authentication.services import AuthenticationService, UserService
from src.authentication.use_cases import (
    LoginUserUseCase,
    LogoutUserUseCase,
    RefreshTokenUseCase,
    RegisterUserUseCase,
)


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(UserRepository, UserRepository)

    container.register(UserService, UserService)
    container.register(AuthenticationService, AuthenticationService)

    container.register(RegisterUserUseCase, RegisterUserUseCase)
    container.register(LoginUserUseCase, LoginUserUseCase)
    container.register(LogoutUserUseCase, LogoutUserUseCase)
    container.register(RefreshTokenUseCase, RefreshTokenUseCase)

    return container


@lru_cache
def get_container() -> punq.Container:
    return _initialize_container()

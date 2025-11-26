from .dto import TokensDTO, UserCredentialsDTO, UserDTO
from .serializers import (
    LoginResponseSerializer,
    RefreshTokenResponseSerializer,
    UserResponseSerializer,
)
from .services import AuthenticationService, UserService


class RegisterUserUseCase:
    def __init__(self, service: UserService, auth_service: AuthenticationService):
        self.service = service
        self.auth_service = auth_service

    def execute(self, dto: UserDTO) -> tuple[UserResponseSerializer, TokensDTO]:
        user = self.service.create_user(dto=dto)
        credentials = UserCredentialsDTO(username=dto.username, password=dto.password)
        tokens = self.auth_service.login(credentials=credentials)
        return UserResponseSerializer.from_dto(dto=user), tokens


class LoginUserUseCase:
    def __init__(self, service: AuthenticationService):
        self.service = service

    def execute(self, credentials: UserCredentialsDTO) -> LoginResponseSerializer:
        tokens = self.service.login(credentials=credentials)
        return LoginResponseSerializer.from_dto(tokens=tokens)


class LogoutUserUseCase:
    def __init__(self, service: AuthenticationService):
        self.service = service

    def execute(self, tokens: TokensDTO) -> None:
        self.service.logout(tokens=tokens)


class RefreshTokenUseCase:
    def __init__(self, service: AuthenticationService):
        self.service = service

    def execute(self, tokens: TokensDTO) -> RefreshTokenResponseSerializer:
        new_tokens = self.service.refresh_token(tokens=tokens)
        return RefreshTokenResponseSerializer.from_dto(tokens=new_tokens)

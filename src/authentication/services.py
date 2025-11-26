from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .dto import TokensDTO, UserCredentialsDTO, UserDTO
from .exceptions import AuthenticationError, InvalidPassword, InvalidToken, UserNotFound
from .repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, dto: UserDTO) -> UserDTO:
        return self.repository.create(dto=dto)


class AuthenticationService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def authenticate_user(self, credentials: UserCredentialsDTO):
        user = self.repository.get_user_by_username(credentials=credentials)
        if not user:
            raise UserNotFound
        if not user.check_password(raw_password=credentials.password):
            raise InvalidPassword
        return user

    def login(self, credentials: UserCredentialsDTO) -> TokensDTO:
        user = self.authenticate_user(credentials=credentials)
        if not user:
            raise AuthenticationError
        token = RefreshToken.for_user(user)
        return TokensDTO(access=str(token.access_token), refresh=str(token))

    @staticmethod
    def logout(tokens: TokensDTO) -> None:
        token = RefreshToken(token=tokens.refresh)
        token.blacklist()

    def refresh_token(self, tokens: TokensDTO) -> TokensDTO:
        try:
            refresh_token = RefreshToken(token=tokens.refresh)
            new_access_token = refresh_token.access_token
            return TokensDTO(access=str(new_access_token), refresh=str(refresh_token))
        except TokenError:
            raise InvalidToken

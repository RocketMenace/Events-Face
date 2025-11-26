from rest_framework import serializers

from .dto import TokensDTO, UserCredentialsDTO, UserDTO


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        min_length=2,
        max_length=50,
        label="Username",
        help_text="username",
    )

    def to_dto(self) -> UserDTO:
        return UserDTO(**self.validated_data)


class UserRequestSerializer(UserBaseSerializer):
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        max_length=50,
        label="Password",
        help_text="password",
    )


class UserResponseSerializer(UserBaseSerializer):
    id = serializers.UUIDField(label="ID", help_text="id")
    username = serializers.CharField(
        required=True,
        min_length=2,
        max_length=50,
    )

    @classmethod
    def from_dto(cls, dto: UserDTO) -> "UserResponseSerializer | None":
        serializer = cls(
            data={
                "id": dto.id,
                "username": dto.username,
            },
        )
        if serializer.is_valid(raise_exception=True):
            return serializer
        return None


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def to_dto(self) -> UserCredentialsDTO:
        return UserCredentialsDTO(**self.validated_data)


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

    @classmethod
    def from_dto(cls, tokens: TokensDTO) -> "LoginResponseSerializer | None":
        serializer = cls(
            data={
                "access_token": tokens.access,
                "refresh_token": tokens.refresh,
            },
        )
        if serializer.is_valid(raise_exception=True):
            return serializer
        return None


class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def to_dto(self) -> TokensDTO:
        return TokensDTO(**self.validated_data)


class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def to_dto(self) -> TokensDTO:
        return TokensDTO(refresh=self.validated_data["refresh"])


class RefreshTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    @classmethod
    def from_dto(cls, tokens: TokensDTO) -> "RefreshTokenResponseSerializer | None":
        serializer = cls(
            data={
                "access_token": tokens.access,
            },
        )
        if serializer.is_valid(raise_exception=True):
            return serializer
        return None

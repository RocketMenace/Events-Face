from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..common.response_factory import api_response_factory
from .api_docs import (
    login_user_docs,
    logout_user_docs,
    refresh_token_docs,
    register_user_docs,
)
from .ioc_container import get_container
from .serializers import (
    LoginRequestSerializer,
    LogoutRequestSerializer,
    RefreshTokenRequestSerializer,
    UserRequestSerializer,
)
from .use_cases import (
    LoginUserUseCase,
    LogoutUserUseCase,
    RefreshTokenUseCase,
    RegisterUserUseCase,
)


@register_user_docs
class UserCreateAPI(APIView):
    def post(
        self,
        request: Request,
    ) -> Response:
        input_serializer = UserRequestSerializer(data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            container = get_container()
            use_case: RegisterUserUseCase = container.resolve(RegisterUserUseCase)
            response, tokens = use_case.execute(dto=input_serializer.to_dto())
            return api_response_factory(
                serializer_class=response,
                status_code=status.HTTP_201_CREATED,
                meta={
                    "message": "User created successfully",
                    "access_token": tokens.access,
                    "refresh_token": tokens.refresh,
                },
            )
        return api_response_factory(
            errors=input_serializer.errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@login_user_docs
class LoginAPI(APIView):
    def post(self, request: Request) -> Response:
        input_serializer = LoginRequestSerializer(data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            container = get_container()
            use_case: LoginUserUseCase = container.resolve(LoginUserUseCase)
            response = use_case.execute(credentials=input_serializer.to_dto())
            return api_response_factory(
                serializer_class=response,
                status_code=status.HTTP_200_OK,
            )
        return api_response_factory(
            errors=input_serializer.errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@logout_user_docs
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        input_serializer = LogoutRequestSerializer(data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            container = get_container()
            use_case: LogoutUserUseCase = container.resolve(LogoutUserUseCase)
            use_case.execute(tokens=input_serializer.to_dto())
            return api_response_factory(
                meta={"message": "Successfully logged out"},
                status_code=status.HTTP_200_OK,
            )
        return api_response_factory(
            errors=input_serializer.errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@refresh_token_docs
class RefreshAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        input_serializer = RefreshTokenRequestSerializer(data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            container = get_container()
            use_case: RefreshTokenUseCase = container.resolve(RefreshTokenUseCase)
            response = use_case.execute(tokens=input_serializer.to_dto())
            return api_response_factory(
                serializer_class=response,
                status_code=status.HTTP_200_OK,
            )
        return api_response_factory(
            errors=input_serializer.errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

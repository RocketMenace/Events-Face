from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status

from .serializers import (
    LoginRequestSerializer,
    LoginResponseSerializer,
    LogoutRequestSerializer,
    RefreshTokenRequestSerializer,
    RefreshTokenResponseSerializer,
    UserRequestSerializer,
    UserResponseSerializer,
)

register_user_docs = extend_schema(
    description=_("Create a new user account."),
    tags=["Auth"],
    methods=["POST"],
    summary=_("Register user"),
    request=UserRequestSerializer,
    examples=[
        OpenApiExample(
            name="Registration payload",
            value={
                "username": "jane_doe",
                "password": "SecurePass123",
            },
            request_only=True,
        ),
    ],
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description=_("User successfully created."),
            response=UserResponseSerializer,
            examples=[
                OpenApiExample(
                    name="User created",
                    value={
                        "data": {
                            "id": "4f5c2ad8-8c7a-4f3c-9d1a-8b4a9b0c1234",
                            "username": "jane_doe",
                        },
                        "meta": {
                            "message": "User created successfully",
                            "access_token": "",
                            "refresh_token": "",
                        },
                        "errors": [],
                    },
                    response_only=True,
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description=_("User with this username already exists."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="User already exists",
                    value={
                        "detail": "User with this username already exists",
                        "code": "error",
                    },
                    response_only=True,
                ),
            ],
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: OpenApiResponse(
            description=_("Validation failed."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="Invalid registration payload",
                    value={
                        "data": {},
                        "meta": {},
                        "errors": [
                            {
                                "field": "username",
                                "messages": [
                                    "Ensure this field has at least 2 characters.",
                                ],
                            },
                            {
                                "field": "password",
                                "messages": [
                                    "Ensure this field has at least 8 characters.",
                                ],
                            },
                        ],
                    },
                    response_only=True,
                ),
            ],
        ),
    },
)

login_user_docs = extend_schema(
    description=_("Authenticate an existing user and issue JWT tokens."),
    tags=["Auth"],
    methods=["POST"],
    summary=_("Login user"),
    request=LoginRequestSerializer,
    examples=[
        OpenApiExample(
            name="Login payload",
            value={
                "username": "jane_doe",
                "password": "SecurePass123",
            },
            request_only=True,
        ),
    ],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description=_("Login successful."),
            response=LoginResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Login success",
                    value={
                        "data": {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        },
                        "meta": {},
                        "errors": [],
                    },
                    response_only=True,
                ),
            ],
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: OpenApiResponse(
            description=_("Validation failed."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="Invalid login payload",
                    value={
                        "data": {},
                        "meta": {},
                        "errors": [
                            {
                                "field": "username",
                                "messages": ["This field may not be blank."],
                            },
                        ],
                    },
                    response_only=True,
                ),
            ],
        ),
    },
)

logout_user_docs = extend_schema(
    description=_("Invalidate the current JWT pair to terminate the session."),
    tags=["Auth"],
    methods=["POST"],
    summary=_("Logout user"),
    request=LogoutRequestSerializer,
    examples=[
        OpenApiExample(
            name="Logout payload",
            value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
            request_only=True,
        ),
    ],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description=_("Logout successful."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="Logout success",
                    value={
                        "data": {},
                        "meta": {"message": "Successfully logged out"},
                        "errors": [],
                    },
                    response_only=True,
                ),
            ],
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description=_("Authentication credentials were not provided or invalid."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="Unauthorized",
                    value={
                        "detail": "Given token not valid for any token type",
                        "code": "token_not_valid",
                    },
                    response_only=True,
                ),
            ],
        ),
    },
)

refresh_token_docs = extend_schema(
    description=_("Issue a new access token using a valid refresh token."),
    tags=["Auth"],
    methods=["POST"],
    summary=_("Refresh access token"),
    request=RefreshTokenRequestSerializer,
    examples=[
        OpenApiExample(
            name="Refresh payload",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            },
            request_only=True,
        ),
    ],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description=_("Access token refreshed."),
            response=RefreshTokenResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Refresh success",
                    value={
                        "data": {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        },
                        "meta": {},
                        "errors": [],
                    },
                    response_only=True,
                ),
            ],
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: OpenApiResponse(
            description=_("Validation failed."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="Invalid refresh payload",
                    value={
                        "data": {},
                        "meta": {},
                        "errors": [
                            {
                                "field": "refresh",
                                "messages": ["This field may not be blank."],
                            },
                        ],
                    },
                    response_only=True,
                ),
            ],
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description=_("Refresh token is invalid or expired."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="Invalid refresh token",
                    value={
                        "detail": "Token is blacklisted",
                        "code": "token_not_valid",
                    },
                    response_only=True,
                ),
            ],
        ),
    },
)

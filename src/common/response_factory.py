from typing import Any

from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .serializer import APIResponseSerializer


def api_response_factory(
    *,
    serializer_class: Serializer | None = None,
    meta: dict[str, Any] | None = None,
    errors: list[dict[str, Any]] | None = None,
    pagination: dict[str, Any] | None = None,
    status_code=None,
) -> Response:
    serialized_data = None
    if serializer_class:
        try:
            serialized_data = serializer_class.data
        except (AttributeError, KeyError):
            serialized_data = getattr(serializer_class, "validated_data", None)

    response_data = {
        "data": serialized_data if serialized_data is not None else {},
        "meta": meta or {},
        "errors": errors or [],
    }

    if pagination:
        response_data["pagination"] = pagination

    api_response_serializer = APIResponseSerializer(data=response_data)
    if api_response_serializer.is_valid(raise_exception=True):
        return Response(
            data=api_response_serializer.validated_data,
            status=status_code,
        )

    return Response(
        data=response_data,
        status=status_code,
    )

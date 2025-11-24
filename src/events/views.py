from urllib.request import Request

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..common.response_factory import api_response_factory
from .api_docs import create_event_area_docs, create_event_docs
from .ioc_container import get_container
from .serializers import EventAreaRequestSerializer, EventRequestSerializer
from .use_cases import CreateAreaUseCase, CreateEventUseCase, GetEventsUseCase


@create_event_area_docs
class EventAreaCreateAPI(APIView):
    def post(self, request: Request) -> Response:
        input_serializer = EventAreaRequestSerializer(data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            container = get_container()
            use_case: CreateAreaUseCase = container.resolve(CreateAreaUseCase)
            response = use_case.execute(dto=input_serializer.to_dto())
            return api_response_factory(
                serializer_class=response,
                status_code=status.HTTP_201_CREATED,
            )
        return api_response_factory(
            errors=input_serializer.errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@create_event_docs
class EventCreateAPI(APIView):
    def post(self, request: Request) -> Response:
        input_serializer = EventRequestSerializer(data=request.data)
        if input_serializer.is_valid(raise_exception=True):
            container = get_container()
            use_case: CreateEventUseCase = container.resolve(CreateEventUseCase)
            response = use_case.execute(dto=input_serializer.to_dto())
            return api_response_factory(
                serializer_class=response,
                status_code=status.HTTP_201_CREATED,
            )
        return api_response_factory(
            errors=input_serializer.errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class ListEventAPI(APIView):
    def get(self, request: Request) -> Response:
        container = get_container()
        use_case: GetEventsUseCase = container.resolve(GetEventsUseCase)
        response = use_case.execute()
        return api_response_factory(
            serializer_class=response,
            status_code=status.HTTP_200_OK,
        )

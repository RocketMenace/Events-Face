from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status

from .serializers import (
    EventAreaRequestSerializer,
    EventAreaResponseSerializer,
    EventRequestSerializer,
    EventResponseSerializer,
    SignUpForEventRequestSerializer,
)

get_events_docs = extend_schema(
    description=_("Retrieve a list of available events."),
    tags=["Events"],
    methods=["GET"],
    summary=_("List events"),
    parameters=[
        OpenApiParameter(
            name="limit",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Number of results to return per page."),
            required=False,
        ),
        OpenApiParameter(
            name="offset",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("The initial index from which to return the results."),
            required=False,
        ),
        OpenApiParameter(
            name="name",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Filter events by name (case-insensitive partial match)."),
            required=False,
        ),
        OpenApiParameter(
            name="order_by",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_(
                "Sort events by event_datetime. Use 'asc' for ascending or 'desc' for descending. Default is 'desc'.",
            ),
            required=False,
            enum=["asc", "desc"],
        ),
    ],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description=_("Successfully retrieved events."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="Events list",
                    value={
                        "data": [
                            {
                                "id": "ae764a1e-5960-4f70-b39b-9a2dbce9c2cf",
                                "name": "Tech Conference 2025",
                                "area": "Main Hall",
                                "status": "open",
                                "event_datetime": "01.13.2026",
                                "registration_deadline": "01.13.2026",
                            },
                            {
                                "id": "ae987a1e-5960-4f70-b39b-9a2dbce9c2cf",
                                "name": "Tech Conference 2026",
                                "area": "Main Hall",
                                "status": "open",
                                "event_datetime": "01.13.2026",
                                "registration_deadline": "01.13.2026",
                            },
                        ],
                        "meta": {},
                        "errors": [],
                        "pagination": {
                            "offset": 0,
                            "limit": 10,
                            "total": 18,
                        },
                    },
                    response_only=True,
                ),
            ],
        ),
    },
)


create_event_docs = extend_schema(
    description=_("Create a new event in a specific event area."),
    tags=["Events"],
    methods=["POST"],
    summary=_("Create event"),
    request=EventRequestSerializer,
    examples=[
        OpenApiExample(
            name="Example request",
            value={
                "name": "Tech Conference 2025",
                "area_id": "1c74b3ec-b651-4775-88b6-8b21f37fc3f4",
                "status": "open",
                "event_datetime": "01.13.2026",
                "registration_deadline": "01.13.2026",
            },
            request_only=True,
        ),
    ],
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description=_("Event successfully created."),
            response=EventResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Event created",
                    value={
                        "data": {
                            "id": "ae764a1e-5960-4f70-b39b-9a2dbce9c2cf",
                            "name": "Tech Conference 2025",
                            "area": "1c74b3ec-b651-4775-88b6-8b21f37fc3f4",
                            "status": "open",
                            "event_datetime": "01.13.2026",
                            "registration_deadline": "01.13.2026",
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
                    name="Invalid payload",
                    value={
                        "data": {},
                        "meta": {},
                        "errors": [
                            {
                                "field": "area",
                                "messages": ["Event area does not exist."],
                            },
                            {
                                "field": "event_datetime",
                                "messages": ["Event datetime cannot be in the past."],
                            },
                        ],
                    },
                    response_only=True,
                ),
            ],
        ),
    },
)

create_event_area_docs = extend_schema(
    description=_("Create a new event area that can be used to group events."),
    tags=["Areas"],
    methods=["POST"],
    summary=_("Create event area"),
    request=EventAreaRequestSerializer,
    examples=[
        OpenApiExample(
            name="Example request",
            value={
                "name": "Main Hall",
            },
            request_only=True,
        ),
    ],
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description=_("Event area successfully created."),
            response=EventAreaResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Event area created",
                    value={
                        "data": {
                            "id": "1c74b3ec-b651-4775-88b6-8b21f37fc3f4",
                            "name": "Main Hall",
                        },
                        "meta": {"detail": "Event area created."},
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
                    name="Missing name",
                    value={
                        "data": {},
                        "meta": {},
                        "errors": [
                            {
                                "field": "name",
                                "messages": ["This field is required."],
                            },
                        ],
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="Too long name",
                    value={
                        "data": {},
                        "meta": {},
                        "errors": [
                            {
                                "field": "name",
                                "messages": [
                                    "Ensure this field has no more than 255 characters.",
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

sign_up_for_event_docs = extend_schema(
    description=_(
        "Register a visitor for a specific event by providing their full name and email.",
    ),
    tags=["Events"],
    methods=["POST"],
    summary=_("Sign up for event"),
    parameters=[
        OpenApiParameter(
            name="event_id",
            type=str,
            location=OpenApiParameter.PATH,
            description=_("UUID of the event to register for."),
            required=True,
        ),
    ],
    request=SignUpForEventRequestSerializer,
    examples=[
        OpenApiExample(
            name="Example request",
            value={
                "full_name": "John Doe",
                "email": "john.doe@example.com",
            },
            request_only=True,
        ),
    ],
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description=_("Visitor successfully registered for the event."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="Registration successful",
                    value={
                        "data": {},
                        "meta": {"message": "Successful registration"},
                        "errors": [],
                    },
                    response_only=True,
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description=_("Bad request errors."),
            response=dict,
            examples=[
                OpenApiExample(
                    name="Event is closed",
                    value={
                        "detail": "Event is closed",
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="Registration already exists",
                    value={
                        "detail": "Registration already exists",
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
                    name="Missing required fields",
                    value={
                        "data": {},
                        "meta": {},
                        "errors": [
                            {
                                "field": "full_name",
                                "messages": ["This field is required."],
                            },
                            {
                                "field": "email",
                                "messages": ["This field is required."],
                            },
                        ],
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="Invalid email format",
                    value={
                        "data": {},
                        "meta": {},
                        "errors": [
                            {
                                "field": "email",
                                "messages": ["Enter a valid email address."],
                            },
                        ],
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="Name too long",
                    value={
                        "data": {},
                        "meta": {},
                        "errors": [
                            {
                                "field": "full_name",
                                "messages": [
                                    "Ensure this field has no more than 128 characters.",
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

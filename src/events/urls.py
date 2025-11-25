from django.urls import path

from .apps import EventsConfig
from .views import EventAreaCreateAPI, EventCreateAPI, ListEventAPI

app_name = EventsConfig.name

urlpatterns = [
    path("list", ListEventAPI.as_view(), name="event-list"),
    path("", EventCreateAPI.as_view(), name="event-create"),
    path("areas/", EventAreaCreateAPI.as_view(), name="event-area-create"),
]

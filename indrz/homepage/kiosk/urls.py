from django.conf.urls import url

from .views import get_terminal, route_from_terminal

urlpatterns = [
   url(r'^route/(?P<destination_location>.+)', route_from_terminal, name="route from kiosk"),
   url(r'^', get_terminal, name="get kiosk data"),


]
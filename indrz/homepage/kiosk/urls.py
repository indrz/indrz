from django.conf.urls import url

from .views import getPoiTerminalData, route_from_terminal

urlpatterns = [
   url(r'^route/.+', route_from_terminal, name="route from kiosk"),
   url(r'(?P<kiosk_id>.+)', getPoiTerminalData, name="get kiosk data"),


]
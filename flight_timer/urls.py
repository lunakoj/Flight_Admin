from django.urls import path
from . import views

app_name = 'flight_timer'

urlpatterns = [
    path('flight_hours/', views.flight_hours, name = 'flight_hours'),
]

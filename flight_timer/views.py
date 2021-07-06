from django.shortcuts import render
from flight_timer.models import Pilot_flight_hours

# Create your views here.
def index(request):
    return render(request, 'flight_timer/index.html')

def flight_hours(request):

    flight_hour_list =  Pilot_flight_hours.objects.order_by('flight_icao')
    flight_hour_dict = {'flight_hour': flight_hour_list}
    return render(request, 'flight_timer/flight_hours.html', context=flight_hour_dict)
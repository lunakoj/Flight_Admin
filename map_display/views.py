from django.shortcuts import render, get_object_or_404
from .util import check_flights
from .models import MapDisplay
from .forms import Display_form
import folium
import airportsdata


airports = airportsdata.load('IATA')  # key is IATA code


# Create your views here.

def display(request):
    # obj  = get_object_or_404(MapDisplay, id= 1)
    # Initiate Folium
    m = folium.Map(width=800, height=500, location= (airports['ABV']['lat'],airports['ABV']['lon']), zoom_start=6.5)
    # Location maker
    folium.Marker((airports['ABV']['lat'],airports['ABV']['lon']), tooltip='click for more', popup= airports['ABV']['name'],).add_to(m)
    form = Display_form(request.POST or None)
    e = ''

    if form.is_valid():
        instance = form.save(commit=False)
        flights = check_flights(form.cleaned_data.get('airline_icao'))

        if len(flights) >= 1:
            print(flights)
            # Initiate Folium
            m = folium.Map(width=800, height=500, location= (airports['ABV']['lat'],airports['ABV']['lon']), zoom_start=6.5)

            for data in range(len(flights)):
                MapDisplay.objects.get_or_create(airline_icao = form.cleaned_data.get('airline_icao'), aircraft_reg = flights[data].registration, origin_airport = flights[data].origin_airport_iata, destination_airport = flights[data].destination_airport_iata, long = flights[data].longitude, lat = flights[data].latitude)[0]
                # Location maker
                folium.Marker((flights[data].latitude,flights[data].longitude), tooltip= flights[data].registration, popup= get_object_or_404(MapDisplay, aircraft_reg = flights[data].registration), 
                                icon = folium.Icon(color='red', icon='plane', prefix='fa')).add_to(m)
                # # fetch flight info object from database
                # flight_info_list = MapDisplay.objects.order_by('created')
        else:
            e = "No flight for Airline at the moment"
    else:
        e = "Please input the correct Airline ICAO Code"

    # fetch flight info object from database
    flight_info_list = MapDisplay.objects.order_by('created')

    # format map for html representation
    m = m._repr_html_()

    context = {
        'error': e,
        'form' : form ,
        'flight_info':flight_info_list,
        'to_view' : m,
        }
    return render(request, 'map_display/display.html', context)

from django.shortcuts import render, get_object_or_404
from .util import check_flights
from .models import MapDisplay
from .forms import Display_form
import folium
import airportsdata


airports = airportsdata.load('IATA')  # key is IATA code
airports_b = airportsdata.load()  # key is ICAO code
ng_airports_icao = ["DN50", "DN51", "DN53", "DN54", "DN55", "DN56", "DNAA", "DNAK", "DNAS",
 "DNBE", "DNBI", "DNCA", "DNEN", "DNGO", "DNIB", "DNIL", "DNIM", "DNJO", "DNKA", "DNKN", "DNMA", "DNMK", 
"DNMM", "DNMN", "DNOS", "DNPO", "DNSO", "DNTZ", "DNYO", "DNZA"]

# Create your views here.

def display(request):
    # Initiate Folium
    m = folium.Map(width=800, height=500, location= (airports['ABV']['lat'],airports['ABV']['lon']), zoom_start=6.5)

    # Location maker
    folium.Marker((airports['ABV']['lat'],airports['ABV']['lon']), tooltip='click for more', popup= airports['ABV']['name'],).add_to(m)
    fg = folium.FeatureGroup(name="My Map")
    for _ in ng_airports_icao:
        fg.add_child(folium.Marker((airports_b[_]['lat'],airports_b[_]['lon']), tooltip=airports_b[_]['iata'], popup= airports_b[_]['name'],icon = folium.Icon(icon='plane', prefix='fa')))
    m.add_child(fg)

    form = Display_form(request.POST or None)
    e = ''

    if form.is_valid():
        instance = form.save(commit=False)
        flights = check_flights(form.cleaned_data.get('airline_icao'))

        if len(flights) >= 1:
            print(flights)
            # Initiate Folium
            m = folium.Map(width=800, height=500, location= (airports['ABV']['lat'],airports['ABV']['lon']), zoom_start=6.5)
            fg = folium.FeatureGroup(name="My Map")

            for data in range(len(flights)):
                # Output MapDisplay objects from the database
                MapDisplay.objects.get_or_create(airline_icao = form.cleaned_data.get('airline_icao'), aircraft_reg = flights[data].registration, origin_airport = flights[data].origin_airport_iata, destination_airport = flights[data].destination_airport_iata, long = flights[data].longitude, lat = flights[data].latitude)[0]
                # flight position  maker
                fg.add_child(folium.Marker((flights[data].latitude,flights[data].longitude), tooltip= flights[data].registration, popup= get_object_or_404(MapDisplay, aircraft_reg = flights[data].registration), icon = folium.features.CustomIcon('./static/images/plane11.png', icon_size = (25,25))))
            m.add_child(fg)
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

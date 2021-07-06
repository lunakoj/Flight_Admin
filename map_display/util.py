from FlightRadar24.api import FlightRadar24API



def check_flights(airline_icao):
    try:
        fr_api = FlightRadar24API()
    except [ConnectionError, ConnectionResetError] as e:
        print(e)
        fr_api = "No Response! Please try connection after 120 sec"

    if fr_api != "No Response!":
        # airline_icao = "UAE"
        flights = fr_api.get_flights(airline = airline_icao)
        # now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    else:
        return fr_api
    return flights

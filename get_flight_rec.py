import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_admin.settings')

import django
django.setup()

from FlightRadar24.api import FlightRadar24API
import threading, time, signal
from datetime import timedelta, datetime
from flight_timer.models import Pilot_flight_hours


try:
    fr_api = FlightRadar24API()
except [ConnectionError, ConnectionResetError] as e:
    print(e)
    fr_api = "No Response!"



WAIT_TIME_SECONDS = 70

class ProgramKilled(Exception):
    pass

def check_flights():
    airline_icao = "UAE"
    flights = fr_api.get_flights(airline = airline_icao)
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    f_record = {}
    # print(flights)

    if len(flights) >= 1:
        for data in range(len(flights)):

            if (flights[data].registration in f_record) and (flights[data].ground_speed <= 50) :
                f_record[flights[data].registration] = [f_record[flights[data].registration], now]
                # Parameter check console print out before data entry
                print("{}'s Flight {} took of at: {} and landed at: {}. flight hours: {}".format(flights[data].airline_icao, flights[data].registration, f_record[flights[data].registration][0], f_record[flights[data].registration][1], f_record[flights[data].registration][1] - f_record[flights[data].registration][0]))
                # New Flight Data Entry
                flight_data = Pilot_flight_hours.objects.get_or_create(flight_icao = flights[data].registration, takeoff_time = f_record[flights[data].registration][0], landing_time = f_record[flights[data].registration][1], flight_hours = f_record[flights[data].registration][1] - f_record[flights[data].registration][0])[0]

                del f_record[flights[data].registration]

            elif (flights[data].registration not in f_record) and (flights[data].altitude <= 10) and (flights[data].ground_speed >= 100) :
                f_record[flights[data].registration] = now
                print("{}'s flight {} has taken off at {}".format(flights[data].airline_icao, flights[data].registration, now))
            else:
                print("Ground speed for {}'s {} as at {} is: {}, Longitude = {} while Latitude is {}.".format(flights[data].airline_icao, flights[data].registration, now, flights[data].ground_speed,flights[data].longitude,flights[data].latitude))


    else:
        print("No flight for Airline at the moment")



def signal_handler(signum, frame):
    raise ProgramKilled

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(*self.args, **self.kwargs)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=check_flights)
    job.start()

    while True:
          try:
              time.sleep(1)
          except ProgramKilled:
              print("Program killed: running cleanup code")
              job.stop()
              break
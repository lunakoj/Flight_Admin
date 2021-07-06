import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_admin.settings')

import django
django.setup()

from faker import Faker
from flight_timer.models import Pilot_flight_hours
from datetime import timedelta, datetime
import random


fakegen = Faker()

# Air peace Fleet by Flight Registration
air_peace_fleet = ['5N-BQO','5N-BQP','5N-BQU','5N-BQV','5N-BUK','5N-BUL','5N-BQQ','5N-BQR','5N-BQS','5N-BRN','5N-BUJ','5N-BVE','5N-BUU','5N-BWI','5N-BXF','5N-BYF','5N-BYG']

# Estimated flight times in hour
time_of_flight = list(range(1,10))

def add_flight_icao():
    f = random.choice(air_peace_fleet)
    return f

def get_hour():
    t = random.choice(time_of_flight)
    return t

def populate(N=10):

    for entry in range(N):
        # Create the fake data for entry
        fake_company = add_flight_icao()
        fake_flight_takeoff_time = fakegen.date_time()
        fake_flight_landing_time = fakegen.date_time()

        # Create the flight data entry
        flight_data = Pilot_flight_hours.objects.get_or_create(flight_icao = fake_company, takeoff_time = fake_flight_takeoff_time, landing_time = fake_flight_landing_time, flight_hours = fake_flight_landing_time - fake_flight_takeoff_time)[0]
        # print("The Air Peace flight {} took of at {} and landed at {}".format(fake_company, fake_flight_takeoff_time, fake_flight_landing_time))


if __name__ == "__main__":
    # Run the populate function with any number of data
    print('Populating Script Initiated')
    populate(20)
    print('Populating Script Completed')
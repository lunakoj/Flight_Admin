from django.db import models

# Create your models here.
class Pilot_flight_hours(models.Model):
    flight_icao = models.CharField(max_length=25)
    takeoff_time = models.DateTimeField()
    landing_time = models.DateTimeField()
    flight_hours = models.DurationField()
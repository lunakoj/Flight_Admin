from django.db import models

# Create your models here.


class MapDisplay(models.Model):
    airline_icao = models.CharField(max_length=200)
    aircraft_reg = models.CharField(max_length=200)
    origin_airport = models.CharField(max_length=200)
    destination_airport = models.CharField(max_length=200)
    long = models.DecimalField(max_digits=10, decimal_places=4)
    lat = models.DecimalField(max_digits=10, decimal_places=4)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"The {self.airline_icao} flight with registration number {self.aircraft_reg} flying from {self.origin_airport} to {self.destination_airport} is currently at longitude, latitude of {self.long},{self.lat} as at {self.created}."
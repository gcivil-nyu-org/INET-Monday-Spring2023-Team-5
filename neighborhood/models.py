from django.db import models


class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    borough = models.CharField(max_length=50)
    description = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    population = models.PositiveIntegerField(null=True)
    crime_count = models.PositiveIntegerField(null=True)
    noise_count = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name

    def get_geopoint(self):
        return "POINT(%s %s)" % (self.lon, self.lat)

    def crime_rate(self):
        if self.population and self.crime_count:
            crime_rate = self.crime_count / self.population * 100
            return "{:.2%}".format(crime_rate)
        else:
            return "N/A"

from django.db import models


class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    borough = models.CharField(max_length=50)
    description = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return self.name

    def get_geopoint(self):
        return "POINT(%s %s)" % (self.lon, self.lat)

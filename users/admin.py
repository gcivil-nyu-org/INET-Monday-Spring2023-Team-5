from django.contrib import admin

from .models import Business, Listing, Neighborhood


admin.site.register(Business)
admin.site.register(Listing)
admin.site.register(Neighborhood)

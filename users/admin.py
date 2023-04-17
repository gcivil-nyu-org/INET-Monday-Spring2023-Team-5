from django.contrib import admin

from users.services.models import Business
from users.marketplace.models import Listing


admin.site.register(Business)
admin.site.register(Listing)

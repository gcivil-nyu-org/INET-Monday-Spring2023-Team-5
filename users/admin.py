from django.contrib import admin

from users.marketplace.models import Listing
from users.services.models import Business


admin.site.register(Business)
admin.site.register(Listing)

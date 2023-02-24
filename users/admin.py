from django.contrib import admin

# Register your models here.

from .models import User, Business

admin.site.register(User)
admin.site.register(Business)

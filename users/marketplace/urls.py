from django.urls import path

from users.marketplace import views


urlpatterns = [
    path("", views.listings, name="user_listings"),
    path("add/", views.add, name="add_listing"),
    path("<int:listing_id>/", views.view, name="view_listing"),
]

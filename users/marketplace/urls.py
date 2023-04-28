from django.urls import path

from users.marketplace import views


urlpatterns = [
    path("", views.my_listings, name="user_listings"),
    path("add/", views.add, name="add_listing"),
    path("<int:listing_id>/", views.view, name="view_listing"),
    path("<int:listing_id>/delete/", views.delete, name="delete_listing"),
    path("<int:listing_id>/update/", views.update, name="update_listing"),
]

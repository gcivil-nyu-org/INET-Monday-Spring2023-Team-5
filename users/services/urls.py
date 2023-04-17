from django.urls import path

from users.services import views

urlpatterns = [
    path("", views.businesses, name="user_businesses"),
    path("add/", views.add, name="add_business"),
    path("<int:business_id>/", views.view, name="view_business"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.neighborhoods, name="neighborhoods"),
    path("<int:neighborhood_id>", views.neighborhood, name="neighborhood"),
    path("<str:borough>", views.borough, name="borough"),
]

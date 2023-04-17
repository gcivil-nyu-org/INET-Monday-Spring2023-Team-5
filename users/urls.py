from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path("", views.index_view, name="user_dashboard"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("add_business/", views.add_business_view, name="add_business"),
    path(
        "view_business/<int:business_id>/",
        views.view_business_view,
        name="view_business",
    ),
    path("update_password", views.update_password, name="update_password"),
    path("update_user/", views.update_user, name="update_user"),
    path("delete_user/", views.delete_user, name="delete_user"),
    path("listings/", include("users.marketplace.urls")),
    path(
        "services/",
        views.services,
        name="services",
    ),
    path(
        "view_my_businesses/",
        views.view_my_businesses,
        name="view_my_businesses",
    ),
    path(
        "business_details/<int:business_id>/",
        views.view_business_details,
        name="view_business_details",
    ),
]

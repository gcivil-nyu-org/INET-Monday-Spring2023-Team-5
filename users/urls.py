from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path("", views.index_view, name="user_dashboard"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("update_password", views.update_password, name="update_password"),
    path("update_user/", views.update_user, name="update_user"),
    path("delete_user/", views.delete_user, name="delete_user"),
    path("listings/", include("users.marketplace.urls")),
    path("business/", include("users.services.urls")),
]

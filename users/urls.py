from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path("", views.user_account, name="user_account"),
    path("register/", views.account_register, name="account_register"),
    path("login/", views.account_login, name="account_login"),
    path("logout/", views.account_logout, name="account_logout"),
    path("delete/", views.account_delete, name="account_delete"),
    path("update/", views.update_account, name="update_account"),
    path("password/", views.update_password, name="update_password"),
    path("listings/", include("users.marketplace.urls")),
    path("business/", include("users.services.urls")),
]

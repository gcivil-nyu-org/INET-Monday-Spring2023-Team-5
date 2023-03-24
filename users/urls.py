from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
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
    path(
        "view_all_businesses/",
        views.view_all_businesses_view,
        name="view_all_businesses",
    ),
    path(
        "view_my_businesses/",
        views.view_my_businesses,
        name="view_my_businesses",
    ),
    path("add_listing/", views.add_listing, name="add_listing"),
    path("view_listing/<int:listing_id>/", views.view_listing, name="view_listing"),
    path("marketplace/", views.marketplace, name="marketplace"),
]

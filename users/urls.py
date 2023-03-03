from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_business/', views.add_business_view, name='add_business'),
    path('view_business/<int:business_id>/', views.view_business_view, name='view_business'),
    path("update_password", views.update_password, name="update_password"),
    path("updateuser/", views.updateuser, name="updateuser"),
    path("deactivate_user/", views.deactivate_user, name="deactivate_user"),
    path('view_all_businesses/', views.view_all_businesses_view, name='view_all_businesses'),
]

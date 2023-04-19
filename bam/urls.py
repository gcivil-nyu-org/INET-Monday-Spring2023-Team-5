"""bam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from users.marketplace import views as marketplace_views
from users.services import views as services_views

urlpatterns = [
    path("", include("homepage.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("neighborhoods/", include("neighborhood.urls")),
    path("marketplace/", marketplace_views.marketplace, name="marketplace"),
    path(
        "marketplace/<str:borough>",
        marketplace_views.marketplace_by_borough,
        name="marketplace_by_borough",
    ),
    path("services/", services_views.services, name="services"),
    path(
        "services/<str:borough>",
        services_views.services_by_borough,
        name="services_by_borough",
    ),
]

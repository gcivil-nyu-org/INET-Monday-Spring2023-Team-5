import os

from django.shortcuts import render

from .models import Neighborhood
from .utils import get_title

from decouple import config


def neighborhoods(request):
    neighborhoods = Neighborhood.objects.all()

<<<<<<< HEAD
    context = {"neighborhoods": neighborhoods, "page": "neighborhoods", "MAPBOX_API_KEY": os.environ.get('MAPBOX_API_KEY')}
=======
    context = {
        "neighborhoods": neighborhoods,
        "page": "neighborhoods",
        "MAPBOX_API_KEY": config("MAPBOX_API_KEY"),
    }
>>>>>>> fba1830f246c0087a6d34695bce4705065b984a9

    if request.user.is_authenticated:
        context["firstname"] = request.user.first_name

    return render(request, "neighborhoods/index.html", context)


def neighborhood(request, neighborhood_id):
    neighborhood = Neighborhood.objects.get(pk=neighborhood_id)

    context = {
        "neighborhood": neighborhood,
        "page": "neighborhood",
        "MAPBOX_API_KEY": config("MAPBOX_API_KEY"),
    }

    if request.user.is_authenticated:
        context["firstname"] = request.user.first_name

    return render(request, "neighborhoods/neighborhood.html", context)


def borough(request, borough):
    borough = get_title(borough)
    neighborhoods = Neighborhood.objects.filter(borough=borough)

    context = {"borough": borough, "neighborhoods": neighborhoods, "page": "borough"}

    if request.user.is_authenticated:
        context["firstname"] = request.user.first_name

    return render(request, "neighborhoods/borough.html", context)


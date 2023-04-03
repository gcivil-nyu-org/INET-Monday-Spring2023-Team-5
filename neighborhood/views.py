from django.shortcuts import render
from scripts.location import get_neighborhood

def index_view(request):
    if not request.user.is_authenticated:
        return render(request, "neighborhoods/index.html", {"page": "neighborhoods"})

    if request.method == 'POST':
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        neighborhood = get_neighborhood(lat,lon)
        neighborhood.lat = lat
        neighborhood.lon = lon
        neighborhood.save()

    return render(
        request,
        "neighborhoods/index.html",
        {"firstname": "{}".format(request.user.first_name), "page": "neighborhoods"},
    )



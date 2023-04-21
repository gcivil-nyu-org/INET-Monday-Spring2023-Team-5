from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from users.marketplace.models import Listing
from neighborhood.models import Neighborhood

from neighborhood.utils import get_title


@login_required
def marketplace(request):
    listings = Listing.objects.all()

    context = {"listings": listings, "page": "marketplace"}
    context["firstname"] = request.user.first_name

    return render(request, "marketplace/marketplace.html", context)


@login_required
def marketplace_by_borough(request, borough):
    borough = get_title(borough)
    listings = Listing.objects.filter(neighborhood__borough=borough)

    context = {
        "borough": borough,
        "listings": listings,
        "page": "marketplace-by-borough",
    }
    context["firstname"] = request.user.first_name

    return render(request, "marketplace/borough.html", context)


@login_required
def add(request):
    if request.method == "POST":
        neighborhood = Neighborhood.objects.get(pk=request.POST["neighborhood"])
        listing = Listing(
            title=request.POST["title"],
            description=request.POST["description"],
            price=request.POST["price"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            address=request.POST["address"],
            owner=request.user,
            neighborhood=neighborhood,
        )
        listing.save()

        messages.success(request, "Listing added successfully")

        id = listing.id
        return HttpResponseRedirect(reverse("view_listing", args=(id,)))

    neighborhoods = Neighborhood.objects.all()

    context = {"neighborhoods": neighborhoods, "page": "account-add-listing"}
    context["firstname"] = request.user.first_name

    return render(request, "marketplace/add_listing.html", context)


@login_required
def view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    context = {"listing": listing, "page": "listing"}
    context["firstname"] = request.user.first_name

    return render(request, "marketplace/view_listing.html", context)

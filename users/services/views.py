from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect

from users.services.models import Business
from neighborhood.models import Neighborhood

from neighborhood.utils import get_title


def services(request):
    businesses = Business.objects.all()

    context = {"businesses": businesses, "page": "services"}

    if request.user.is_authenticated:
        context["firstname"] = request.user.first_name

    return render(request, "services/services.html", context)


@login_required
def services_by_borough(request, borough):
    borough = get_title(borough)
    businesses = Business.objects.filter(neighborhood__borough=borough)

    context = {
        "borough": borough,
        "businesses": businesses,
        "page": "services-by-borough",
    }
    context["firstname"] = request.user.first_name

    return render(request, "services/borough.html", context)


@login_required
def businesses(request):
    businesses = Business.objects.filter(owner=request.user)

    context = {"businesses": businesses, "page": "account-my-businesses"}
    context["firstname"] = request.user.first_name

    return render(request, "services/businesses.html", context)


@login_required
def add(request):
    if request.method == "POST":
        neighborhood = Neighborhood.objects.get(pk=request.POST["neighborhood"])
        business = Business(
            name=request.POST["name"],
            address=request.POST["address"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            neighborhood=neighborhood,
            owner=request.user,
        )
        business.save()

        messages.success(request, "Business added successfully")

        id = business.id
        return HttpResponseRedirect(reverse("view_business", args=(id,)))

    neighborhoods = Neighborhood.objects.all()

    context = {"neighborhoods": neighborhoods, "page": "account-add-business"}
    context["firstname"] = request.user.first_name

    return render(request, "services/add_business.html", context)


@login_required
def view(request, business_id):
    business = Business.objects.get(id=business_id)

    context = {"business": business, "page": "business"}
    context["firstname"] = request.user.first_name

    return render(request, "services/view_business.html", context)

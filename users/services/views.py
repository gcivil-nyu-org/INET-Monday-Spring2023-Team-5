from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect

from users.services.models import Business


def services(request):
    businesses = Business.objects.all()

    context = {"businesses": businesses, "page": "services"}

    if request.user.is_authenticated:
        context["firstname"] = request.user.first_name

    return render(request, "users/services.html", context)


# def filter_by_borough(request, borough):
#     businesses = Business.objects.filter(neighborhood__borough=borough)
#     context = {
#         "borough": borough,
#         "businesses": businesses,
#         "page": "services by borough",
#     }
#     if request.user.is_authenticated:
#         context["firstname"] = request.user.first_name
#     return render(request, "services/borough.html", context)


@login_required
def businesses(request):
    businesses = Business.objects.filter(owner=request.user)

    context = {"businesses": businesses, "page": "user businesses"}
    context["firstname"] = request.user.first_name

    return render(request, "services/businesses.html", context)


@login_required
def add(request):
    if request.method == "POST":
        business = Business(
            name=request.POST["name"],
            address=request.POST["address"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            owner=request.user,
        )
        business.save()

        messages.success(request, "Business added successfully")

        id = business.id
        return HttpResponseRedirect(reverse("view_business", args=(id,)))

    context = {"page": "add business"}
    context["firstname"] = request.user.first_name

    return render(request, "services/add_business.html", context)


@login_required
def view(request, business_id):
    business = Business.objects.get(id=business_id)

    context = {"business": business, "page": "view business"}
    context["firstname"] = request.user.first_name

    return render(request, "services/view_business.html", context)


# @login_required
# def edit(request, business):
#     #

#     context = {"page": "edit business"}
#     context["firstname"] = request.user.first_name

#     return render(request, "services/edit_business.html", context)


# @login_required
# def delete(request, business):
#     #

#     context = {"page": "delete business"}
#     context["firstname"] = request.user.first_name

#     return render(request, "services/delete_business.html", context)

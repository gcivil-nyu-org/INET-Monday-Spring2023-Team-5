from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Business


def index_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(
        request,
        "users/index.html",
        {"firstname": "{}".format(request.user.first_name), "page": "user-dashboard"},
    )


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("user_dashboard"))
        else:
            return render(
                request,
                "users/login.html",
                {"message": "Invalid credentials.", "page": "login"},
            )

    return render(request, "users/login.html", {"page": "login"})


def register_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            return render(
                request,
                "users/register.html",
                {"message": "Passwords must match.", "page": "register"},
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "users/register.html",
                {"message": "Email already exists.", "page": "register"},
            )

        user = User.objects.create_user(
            email=email,
            password=password1,
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            username=email,
        )
        user = authenticate(request, username=email, password=password1)

        login(request, user)
        return HttpResponseRedirect(reverse("user_dashboard"))

    return render(request, "users/register.html", {"page": "register"})


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    logout(request)

    return render(
        request, "users/logout.html", {"message": "LOGGED OUT!", "page": "logout"}
    )


def update_user(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not authorized to view this page!")
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method == "POST":
            user = User.objects.get(pk=request.user.pk)
            email = request.POST["email"]
            # Check if the new email is used by any other users or not
            if user.email != email and User.objects.filter(email=email).exists():
                return render(
                    request,
                    "users/update_user.html",
                    {
                        "message": "Email already exists.",
                        "firstname": "{}".format(request.user.first_name),
                        "page": "user-edit",
                    },
                )

            user.username = request.POST["email"]
            user.email = request.POST["email"]
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()
            messages.success(request, "Profile Updated Successfuly.")
            return HttpResponseRedirect(reverse("user_dashboard"))
        else:
            return render(
                request,
                "users/update_user.html",
                {
                    "user": User.objects.get(pk=request.user.pk),
                    "firstname": "{}".format(request.user.first_name),
                    "page": "user-edit",
                },
            )


def update_password(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method == "POST":
            current_password = request.POST["current_password"]
            username = request.user.username
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            if password1 != password2:
                return render(
                    request,
                    "users/update_password.html",
                    {
                        "message": "Passwords must match.",
                        "firstname": "{}".format(request.user.first_name),
                        "page": "user-update-password",
                    },
                )

            u = User.objects.get(pk=request.user.pk)
            if u.check_password(current_password):
                u.set_password(password1)
                u.save()
                login(request, u)
            else:
                return render(
                    request,
                    "users/update_password.html",
                    {
                        "message": "Wrong password",
                        "firstname": "{}".format(request.user.first_name),
                        "page": "user-update-password",
                    },
                )

            return render(
                request,
                "users/update_user.html",
                {
                    "message": "Password Updated Successfuly",
                    "firstname": "{}".format(request.user.first_name),
                    "page": "user-update-password",
                },
            )

        else:
            return render(
                request,
                "users/update_password.html",
                {
                    "firstname": "{}".format(request.user.first_name),
                    "page": "user-update-password",
                },
            )


def delete_user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        password = request.POST["password"]
        u = User.objects.get(pk=request.user.pk)
        if u.check_password(password):
            u.delete()
            return render(
                request,
                "users/logout.html",
                {
                    "message": "Account Deleted",
                    "firstname": "{}".format(request.user.first_name),
                    "page": "user-delete",
                },
            )
        else:
            return render(
                request,
                "users/delete_user.html",
                {
                    "message": "Wrong password",
                    "firstname": "{}".format(request.user.first_name),
                    "page": "user-delete",
                },
            )

    else:
        return render(
            request,
            "users/delete_user.html",
            {"firstname": "{}".format(request.user.first_name), "page": "user-delete"},
        )


def add_business_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        business = Business(
            name=request.POST["name"],
            address=request.POST["address"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            owner=request.user,
        )
        business.save()

        return HttpResponseRedirect(reverse("view_my_businesses"))

    return render(
        request,
        "users/add_business.html",
        {
            "firstname": "{}".format(request.user.first_name),
            "page": "user-add-business",
        },
    )


def view_business_view(request, business_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    business = Business.objects.get(id=business_id)

    return render(
        request,
        "users/view_business.html",
        {
            "message": "View your business.",
            "business": business,
        },
    )


def services(request):
    businesses = Business.objects.all()

    if not request.user.is_authenticated:
        return render(
            request,
            "users/services.html",
            {
                "businesses": businesses,
                "page": "services",
            },
        )

    return render(
        request,
        "users/services.html",
        {
            "businesses": businesses,
            "firstname": "{}".format(request.user.first_name),
            "page": "services",
        },
    )


def view_my_businesses(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    businesses = Business.objects.filter(owner=request.user)

    return render(
        request,
        "users/view_my_businesses.html",
        {
            "businesses": businesses,
            "firstname": "{}".format(request.user.first_name),
            "page": "user-my-businesses",
        },
    )


def view_business_details(request, business_id):
    business = Business.objects.get(id=business_id)

    if not request.user.is_authenticated:
        return render(
            request,
            "users/business_details.html",
            {
                "business": business,
                "page": "business-details",
            },
        )

    return render(
        request,
        "users/business_details.html",
        {
            "business": business,
            "firstname": "{}".format(request.user.first_name),
            "page": "business-details",
        },
    )

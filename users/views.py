from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.decorators.cache import never_cache

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from users.services.models import Business
from users.marketplace.models import Listing


@login_required(redirect_field_name="/")
def user_account(request):
    businesses = Business.objects.filter(owner=request.user)
    listings = Listing.objects.filter(owner=request.user)

    context = {"businesses": businesses, "listings": listings, "page": "user-account"}
    context["firstname"] = request.user.first_name
    return render(request, "users/user_account.html", context)


@never_cache
def account_register(request):
    if request.user.is_authenticated:
        return HttpResponsePermanentRedirect("/")

    if request.method == "POST":
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            context = {"message": "Passwords must match.", "page": "register"}
            return render(request, "users/account_register.html", context)

        if User.objects.filter(email=email).exists():
            context = {"message": "Email already exists.", "page": "register"}
            return render(request, "users/account_register.html", context)

        user = User.objects.create_user(
            email=email,
            password=password1,
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            username=email,
        )
        user = authenticate(request, username=email, password=password1)

        login(request, user)
        return HttpResponseRedirect(reverse("user_account"))

    context = {"page": "register"}
    return render(request, "users/account_register.html", context)


@never_cache
def account_login(request):
    if request.user.is_authenticated:
        return HttpResponsePermanentRedirect("/")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("user_account"))

        context = {"message": "Invalid credentials.", "page": "login"}
        return render(request, "users/account_login.html", context)

    context = {"page": "login"}
    return render(request, "users/account_login.html", context)


def account_logout(request):
    logout(request)

    context = {"message": "You have been logged out.", "page": "logout"}
    return render(request, "users/account_logout.html", context)


def account_delete(request):
    if request.method == "POST":
        password = request.POST["password"]
        user = User.objects.get(pk=request.user.pk)

        if user.check_password(password):
            user.delete()

            context = {"message": "Account Deleted", "page": "account-delete"}
            context["firstname"] = request.user.first_name
            return HttpResponseRedirect(reverse("account_register"))

        context = {
            "message": "Wrong password",
            "page": "account-delete",
        }
        context["firstname"] = request.user.first_name
        return render(request, "users/account_delete.html", context)

    context = {
        "page": "account-delete",
    }
    context["firstname"] = request.user.first_name
    return render(request, "users/account_delete.html", context)


def update_account(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk)
        email = request.POST["email"]

        if user.email != email and User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            user.username = email
            user.email = email
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()

            messages.success(request, "Profile Updated Successfully.")
            return HttpResponseRedirect(reverse("user_account"))

    context = {
        "user": request.user,
        "page": "account-edit",
    }
    context["firstname"] = request.user.first_name
    return render(request, "users/update_account.html", context)


def update_password(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords must match.")
        else:
            user = User.objects.get(pk=request.user.pk)
            if user.check_password(current_password):
                user.set_password(password1)
                user.save()
                login(request, user)
                messages.success(request, "Password Updated Successfully.")
                return HttpResponseRedirect(reverse("user_account"))
            else:
                messages.error(request, "Wrong password")

    context = {
        "page": "account-update-password",
    }
    context["firstname"] = request.user.first_name
    return render(request, "users/update_password.html", context)

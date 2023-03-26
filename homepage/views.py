from django.shortcuts import render


def index_view(request):
    if not request.user.is_authenticated:
        return render(request, "homepage/index.html", {"page": "home"})

    return render(
        request,
        "homepage/index.html",
        {"firstname": "{}".format(request.user.first_name), "page": "home"},
    )

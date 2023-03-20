from django.shortcuts import render


def index_view(request):
    if not request.user.is_authenticated:
        return render(request, "homepage/index.html")

    return render(
        request,
        "homepage/index.html",
        {"welcome": "Welcome {}!".format(request.user.first_name)},
    )

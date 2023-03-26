from django.shortcuts import render


def index_view(request):
    if not request.user.is_authenticated:
        return render(request, "businesses/index.html", {"page": "businesses"})

    return render(
        request,
        "businesses/index.html",
        {"firstname": "{}".format(request.user.first_name), "page": "businesses"},
    )

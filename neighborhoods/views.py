from django.shortcuts import render


def index_view(request):
    if not request.user.is_authenticated:
        return render(request, "neighborhoods/index.html", {"page": "neighborhoods"})

    return render(
        request,
        "neighborhoods/index.html",
        {"firstname": "{}".format(request.user.first_name), "page": "neighborhoods"},
    )

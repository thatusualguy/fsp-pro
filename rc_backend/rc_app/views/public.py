from django.shortcuts import render


def index(request):
    return render(
        request,
        "rc_app/public/index.html",
        {
            "foo": "bar",
        },
        # content_type="application/html",
    )

from django.http import HttpResponse


def test_view(request):
    return HttpResponse("Welcome to the chat application")

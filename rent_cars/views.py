from django.http import HttpResponse


def index(request):
    return HttpResponse("The rent cars app will be here!")

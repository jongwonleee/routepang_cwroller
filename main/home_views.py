from django.http import HttpResponse

def index(request):

    print("home req")

    return HttpResponse("home")
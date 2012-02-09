# Create your views here.
from django.http import HttpResponse

def test(httpRequest):
    return HttpResponse("ok")

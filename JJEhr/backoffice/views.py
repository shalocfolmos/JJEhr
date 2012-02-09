# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from JJEhr.lesson.models import Course
from django.contrib.sites.models import get_current_site



@login_required(login_url='/backoffice/login')
def test(httpRequest):
    return render_to_response('backoffice/index.html')

def login(request):
    currentSite = get_current_site(request)
    next = request.POST["next"]
    form = AuthenticationForm(request.POST)
    if not form.is_valid():
        context = {
            'form': form,
            'next': next,
            'site': currentSite,
            'site_name': current_site.name,
        }
        return render_to_response("/backoffice/login", context,
            context_instance=RequestContext(request, current_app=None))

    username = request.POST["username"]
    password = request.POST["passoword"]
    next = request.POST["next"]
    user = authenticate(username=username,password=password)
    if user is not None and user.is_active:
        login(request,user)
        return HttpResponseRedirect("backoffice/index.html")
    else:
        return HttpResponseRedirect("backoffice/login.html")

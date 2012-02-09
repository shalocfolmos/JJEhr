# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.template import Context,Template, context
from django.template.context import RequestContext

def index(httpRequest):
    reverse('t')
    return render_to_response("lesson/index.html",{"name":'test'},context_instance=RequestContext(httpRequest))

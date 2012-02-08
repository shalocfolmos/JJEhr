# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.template import Context,Template, context

def index(httpRequest):
    t = Template("{{name}}")
    c=Context({"name":"a"})
    return HttpResponse(t.render(c))

#    return render_to_response(t.render(c))

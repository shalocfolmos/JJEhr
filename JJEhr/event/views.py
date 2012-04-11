# Create your views here.
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from JJEhr.event.form import AddEventTypeForm


@login_required(login_url='/backoffice/login')
@csrf_protect
def event_add(request):
    form = AddEventTypeForm(request)
    json_raw_data = dict()
    if form.is_valid():
        form.save()
        json_raw_data['message'] = 'SUCCESS'
    else:
        json_raw_data['message'] = form.errors[0]
    return HttpResponse(json.dumps(json_raw_data), content_type="application/json")


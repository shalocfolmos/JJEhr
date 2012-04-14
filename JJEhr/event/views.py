#-*- coding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from JJEhr.event.form import AddEventTypeForm
from JJEhr.event.models import EventType


@login_required(login_url='/backoffice/login')
@require_http_methods(["POST"])
@csrf_protect
def event_add(request):
    try:
        form = AddEventTypeForm(request.POST)
        if form.is_valid():
            form.save()
            result = u'添加事件类型成功'
        else:
            result = u'参数输入错误,请注意格式,事件类型名称不能为空'
    except Exception, e:
        result = repr(e)
    return HttpResponse(result)


@login_required(login_url='/backoffice/login')
@require_http_methods(["POST"])
@csrf_protect
def event_delete(request):
    event_type = EventType.objects.get(id=request.POST['event_type_id'])
    event_type.delete()



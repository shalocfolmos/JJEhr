#-*- coding: UTF-8 -*-
from StringIO import StringIO
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
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


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def event_show_all(request):
    event_type_list = EventType.objects.all()
    type_name_list = ["<div>" + event_type.type_name + "</div>" for event_type in event_type_list]
    string_io = StringIO()
    for type_name in type_name_list:
        string_io.write(type_name)
    result = string_io.getvalue()
    string_io.close()
    return HttpResponse(result)


@require_http_methods(["GET"])
def ajax_content_html(request):
    form = AddEventTypeForm()
    return render_to_response("event/ajax_content.html", {"eventTypeForm": form})






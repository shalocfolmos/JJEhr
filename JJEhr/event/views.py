#-*- coding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from JJEhr.event.form import AddEventTypeForm
from JJEhr.event.models import EventType

@login_required(login_url='/backoffice/login')
@require_http_methods(["POST"])
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


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def event_delete(request, event_type_id=0):
    if(event_type_id == 0):
        return  HttpResponse("传入参数异常")
    try:
        event_type = EventType.objects.get(id=event_type_id)
        event_type.delete()
        return  HttpResponse("删除事件类型成功")
    except Exception:
        return  HttpResponse("服务器异常，请稍后再试")


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def get_all_event_type(request):
    event_type_list = EventType.objects.all()
    return render_to_response("ajax/ajaxEditEventContent.html", {"event_type_list": event_type_list})


@require_http_methods(["GET"])
def ajax_content_html(request):
    form = AddEventTypeForm()
    return render_to_response("ajax/ajaxAddEventContent.html", {"eventTypeForm": form})






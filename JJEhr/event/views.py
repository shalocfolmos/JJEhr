#-*- coding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from JJEhr.event.form import AddEventTypeForm


@login_required(login_url='/backoffice/login')
@csrf_protect
def event_add(request):
    try:
        if request.method == 'POST':
            form = AddEventTypeForm(request.POST)
            if form.is_valid():
                form.save()
                result = u'添加事件类型成功'
            else:
                result = u'参数输入错误,请注意格式,事件类型名称不能为空'
    except Exception, e:
        result = repr(e)
    return HttpResponse(result)


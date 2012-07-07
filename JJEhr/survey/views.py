#-*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from JJEhr.survey.models import Survey, StaffProfile

@require_http_methods(["POST"])
@login_required(login_url='/backoffice/login')
def create_survey(request):
    survey = Survey(survey_name=request.POST["survey_name"],survey_target=request.POST["survey_target"])
    if survey.survey_target == "ALL":
        querySet = StaffProfile.objects.all()
    else:
        querySet = StaffProfile.objects.get(division=survey.survey_target)
    survey.total_employee_number = querySet.count()
    survey.save()
    result = u'创建问卷成功'
    return HttpResponse(result)


#
#@require_http_methods(["GET"])
#@login_required(login_url='/backoffice/login')
#def list_survey(request):
#    return render_to_response("backoffice/survey_list.html")


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def create_survey_two(request):
    return render_to_response("backoffice/survey_add2.html")


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def preview(request):
    return render_to_response("backoffice/preview.html")
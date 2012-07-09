#-*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from JJEhr.survey.models import Survey, StaffProfile, SurveyItem, SurveyItemAnswer

@require_http_methods(["POST"])
@login_required(login_url='/backoffice/login')
def create_survey(request):
    survey = Survey(survey_name=request.POST["survey_name"], survey_target=request.POST["survey_target"])
    if survey.survey_target == "ALL":
        querySet = StaffProfile.objects.all()
    else:
        querySet = StaffProfile.objects.get(division=survey.survey_target)
    survey.total_employee_number = querySet.count()
    survey.save()
    result = u'创建问卷成功'
    return HttpResponse(result)


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def create_survey_two(request, surveyId, pageNum):
    survey = Survey.objects.get(id=surveyId)
    surveyItemCollection = SurveyItem.objects.filter(survey=survey,page=pageNum)
    for surveyItem in surveyItemCollection:
        surveyItem.answers = SurveyItemAnswer.objects.filter(survey_item=surveyItem)
    return render_to_response("backoffice/survey_add2.html", {"survey": survey, "pageNum": pageNum,"surveyItemCollection":surveyItemCollection})


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def preview(request):
    return render_to_response("backoffice/preview.html")


@require_http_methods(["POST"])
@login_required(login_url='/backoffice/login')
def add_page(request, surveyId):
    survey = Survey.objects.get(id=surveyId)
    if(survey):
        survey.total_page += 1;
        survey.save()
        result = u'添加页面成功'
    else:
        result = u'添加页面失败'
    return HttpResponse(result)


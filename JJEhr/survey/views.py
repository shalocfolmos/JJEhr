#-*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from JJEhr import settings
from JJEhr.survey.models import Survey, StaffProfile, SurveyItem, SurveyItemAnswer, SurveyLog

@require_http_methods(["POST"])
@login_required(login_url='/backoffice/login')
def create_survey(request):
    survey = Survey(survey_name=request.POST["survey_name"], survey_target=request.POST["survey_target"])
    if survey.survey_target == "ALL":
        querySet = StaffProfile.objects.all()
    else:
        querySet = StaffProfile.objects.get(division=survey.survey_target)
    survey.total_employee_number = querySet.count()
    survey.update()
    result = u'创建问卷成功'
    return HttpResponse(result)


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def edit_survey(request, surveyId, pageNum):
    survey = Survey.objects.get(id=surveyId)
    surveyItemCollection = SurveyItem.objects.filter(survey=survey,page=pageNum)
    for surveyItem in surveyItemCollection:
        surveyItem.answers = SurveyItemAnswer.objects.filter(survey_item=surveyItem)
        if surveyItem.item_type == 'METRIX' and surveyItem.answers[0].question_value:
            surveyItem.item_values = surveyItem.answers[0].question_value.split("\n")
    return render_to_response("backoffice/survey_edit.html", {"survey": survey, "pageNum": pageNum,"surveyItemCollection":surveyItemCollection})


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def delete_page(request, surveyId):
    survey = Survey.objects.get(id=surveyId)
    surveyItemCollection = SurveyItem.objects.filter(survey=survey,page=survey.total_page)
    for surveyItem in surveyItemCollection:
        SurveyItemAnswer.objects.filter(survey_item=surveyItem).delete()
    surveyItemCollection.delete()
    if survey.total_page > 1:
        survey.total_page -= 1
        survey.update()
    return HttpResponseRedirect("/backoffice/survey/edit/"+surveyId+"/"+str(1))


@require_http_methods(["POST"])
@login_required(login_url='/backoffice/login')
def create_survey_item(request):
    isRequired = request.POST["isRequired"]

    if isRequired=='false':
        isRequired=False
    else:
        isRequired=True

    surveyItemText = request.POST["surveyItemText"]
    survey_id = request.POST["survey_id"]
    page_num = request.POST["page_num"]
    surveyItemType = request.POST["surveyItemType"]
    survey = Survey.objects.get(id=survey_id)

    if surveyItemType == 'MULTIPLE_CHOICE' or surveyItemType == 'SINGLE_CHOICE' or surveyItemType == 'MULTIPLE_TEXT' or surveyItemType == "METRIX":
        other_answer = request.POST["otherAnswer"]
        if other_answer=='false':
            other_answer=False
        else:
            other_answer=True
        surveyItemAnswer = request.POST["surveyItemAnswer"]
        align_format = request.POST["alignFormat"]
        survey_item = SurveyItem.objects.create(item_type=surveyItemType,item_name=surveyItemText,is_required=isRequired,survey=survey,page=page_num,other_answer=other_answer,align_format=align_format)
        answerCollection = surveyItemAnswer.split("\n")

        for idx,answer in enumerate(answerCollection):
            if request.POST.get("surveyItemAnswerValue"):
                raw_answer_value = request.POST["surveyItemAnswerValue"]
                SurveyItemAnswer.objects.create(question_text=answer,question_value=raw_answer_value,question_sequence=idx,survey_item=survey_item)
            else:
                SurveyItemAnswer.objects.create(question_text=answer,question_value=idx+1,question_sequence=idx,survey_item=survey_item)
    else:
        SurveyItem.objects.create(item_type=surveyItemType,item_name=surveyItemText,is_required=isRequired,survey=survey,page=page_num)
    return HttpResponse("创建成功")



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
        survey.update()
        result = u'添加页面成功'
    else:
        result = u'添加页面失败'
    return HttpResponse(result)

@require_http_methods(["POST"])
@login_required(login_url='/backoffice/login')
def delete_survey_item(request,surveyId=0):
    if surveyId == 0:
        return  HttpResponse(u"参数错误,请重新输入")
    try:
        SurveyItemAnswer.objects.filter(survey_item=surveyId).delete()
        SurveyItem.objects.get(id=surveyId).delete()
    except Exception:
        return  HttpResponse(u"系统异常请重新尝试")
    return  HttpResponse(u"操作成功")


@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def complete_survey(request,surveyId):
    survey = Survey.objects.get(id=surveyId)
    survey.survey_status = 'FINISH'
    survey.update()
    return HttpResponseRedirect("/backoffice/survey/list")



@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def start_survey(request,surveyId):
    survey = Survey.objects.get(id=surveyId)

    surveyLogCollection = SurveyLog.objects.filter(survey=survey)
    for surveyLog in surveyLogCollection:
        try:
            send_mail(subject=request.POST["email_subject"],
                message=request.POST["email_message"],
                from_email=settings.ENROLL_EMAIL_FROM,
                recipient_list=[surveyLog.email],
                fail_silently=False)
            surveyLog.send_email = True
            surveyLog.update()
        except Exception:
            pass
    survey.survey_status = 'CONTINUE'
    survey.update()
    return HttpResponseRedirect("/backoffice/survey/list")


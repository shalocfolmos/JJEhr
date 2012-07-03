from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
@login_required(login_url='/backoffice/login')
def create_survey(request):
    return render_to_response("backoffice/survey_add.html")

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
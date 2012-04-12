from django.forms import forms

class EnrollForm(forms.Form):
    email = forms.EmailField(required=True, label='邮箱')
    course_id = forms.IntegerField(required=True, validators=[validate_enroll], label='课程')

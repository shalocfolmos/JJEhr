from django.core.exceptions import ValidationError

def validate_enroll(value):
    if  value <= 0:
        raise ValidationError(u'%s is not an even number' % value)
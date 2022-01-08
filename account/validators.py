from django.core.exceptions import ValidationError

def validate_email_extension (value):
    valid = (value.endswith('.com') or value.endswith('.ca') or value.endswith('.net') or value.endswith('.org') or value.endswith('.edu') or value.endswith('.jo') or value.endswith('.app'))
    if not valid:
        raise ValidationError ('Invalid E-mail format', code='invalid_email')
    #email = User.objects.filter(email=value)
    #if email is not None:
    #    raise ValidationError('Email is taken', code='email_taken')

def validate_username (value):
    user = User.objects.filter(username=value)
    if user is not None:
        raise ValidationError('Username is taken', code='username_taken')

from django.core.exceptions import ValidationError

def validate_file (value): 
    if value is None:
        raise ValidationError('This field is required', code='empty_video')
    elif not value.endswith('.mp4'):
        raise ValidationError('Invalid file format: videos must be mp4 format!')
    

def validate_image (value):
    if value is None:
        raise ValidationError('This field is required', code='empty_image')
    else:   
        if value.endswith('.jpg') or value.endswith('.png') or value.endswith('.jpeg'):
            pass
        else:
            raise ValidationError('Only accepted image formats are: jpg, jpeg, png')


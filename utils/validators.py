from django.core.exceptions import ValidationError
import re


def form_field_validator(field_name, value):
    if not value:
        return None
    
    if not re.fullmatch(r'^[a-z0-9_.]+$', value):
        raise ValidationError(f'{field_name} must contain only lowercase letters, numbers, underline and dot')
    return value
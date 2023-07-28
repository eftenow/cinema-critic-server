from django.core.exceptions import ValidationError
from datetime import datetime


# Custom Validator
def validate_current_year(value):
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(f'Invalid year! The year cannot be more than {current_year}.')

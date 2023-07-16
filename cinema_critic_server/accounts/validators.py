from django.core.exceptions import ValidationError


def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('File size should not exceed 5MB.')


def name_contains_only_letters(value):
    if not value.isalpha():
        raise ValidationError('This field can only contain letters.')
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.core.exceptions import ValidationError


def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('File size should not exceed 5MB.')


def name_contains_only_letters(value):
    if not value.isalpha():
        raise ValidationError('This field can only contain letters.')


def validate_repeat_password_is_equal(password, repeat_password):
    if password != repeat_password:
        raise ValidationError("Passwords do not match.")

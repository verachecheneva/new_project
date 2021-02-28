from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    current_year = datetime.now().year
    if year > current_year:
        raise ValidationError(
            f'Title cannot be created later than {current_year}'
        )


def validate_scope(scope):
    if scope > 10 or scope < 1:
        raise ValidationError('Score must be from 1 to 10')

from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    current_year = datetime.now().year
    if year > current_year:
        raise ValidationError(
            f'Title cannot be created later than {current_year}'
        )


def validate_score(score):
    if score > 10 or score < 1:
        raise ValidationError('Score must be from 1 to 10')

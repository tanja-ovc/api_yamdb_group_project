from datetime import datetime

from django.core.exceptions import ValidationError


def year_validator(value):
    """Checks that the passed year is not greater than the current year."""
    
    current_year = datetime.now().year
    if value > current_year:
        raise ValidationError(
            'Введите корректное значение в поле "год" '
            f'(не больше {current_year}).'
        )

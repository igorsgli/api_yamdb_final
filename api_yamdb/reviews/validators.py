import datetime

from django.core.exceptions import ValidationError


def no_future_year(value):
    year = datetime.date.today().year
    if value > year:
        raise ValidationError(
            'Введенный год не может быть больше текущего года'
        )

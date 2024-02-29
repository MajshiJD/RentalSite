from django import template
from datetime import datetime, timezone

register = template.Library()


@register.filter(name='get_days')
def get_days(value):
    """
    Custom filter to get the number of days from a datetime.
    """
    now = datetime.now(timezone.utc)
    if value:
        return (now - value).days + 1
    return ''

from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_temp(value):
    try:
        return int(round(float(value),1))
    except:
        return ''


@register.filter
def format_time(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%d.%m.%Y %H:%M")
    except:
        return value

@register.filter
def to_mm_hg(value):
    try:
        return round(float(value) / 1.333, 1)
    except:
        return ''
    

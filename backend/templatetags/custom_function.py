from django import template
from datetime import datetime
from django.utils.timezone import now
import pytz


register = template.Library()

@register.filter
def replace_to_hypen(value):
    return value.replace(" ","-")


@register.filter
def replace_to_space(value):
    return value.replace("-"," ")

@register.filter
def range_to(value):
    return range(value)

@register.filter
def convert_int(value):
    return int(value)

@register.filter
def incr(value):
    return int(value)+1

@register.filter
def fill(value):
    return str(value).zfill(2)

@register.filter
def str_of(value):
    return str(value)

@register.filter
def len_of(value):
    return len(value)

@register.filter
def join_of(value):
    return ", ".join( key for key in value)

@register.filter
def id_Concat(value,arg):
    return str(value + "_" + str(arg))

@register.filter
def get_item_from_list(lst, index):
    try:
        return lst.first()

        
    except (IndexError, ValueError):
        return None
    
@register.filter
def timealert(value, timezone='Asia/Kolkata'):
    value = datetime.fromisoformat(value)
    if not isinstance(value, datetime):
        return value
    target_timezone = pytz.timezone(timezone)
    value = value.astimezone(target_timezone)
    current_time = now().astimezone(target_timezone)
    
    delta = current_time - value

    if delta.days == 0:
        if delta.seconds < 60:
            return "Just Now"
        elif delta.seconds < 3600:
            return f"{delta.seconds // 60} minutes ago"
        else:
            return f"{delta.seconds // 3600} hours ago"
    elif delta.days == 1:
        return "Yesterday"
    else:
        return f"{delta.days} days ago"
    

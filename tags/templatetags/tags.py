from django import template

register = template.Library()

@register.filter
def percentage(value):
    return '{0:.1%}'.format(value)

@register.filter
def dictval(dict, key): 
    if dict and key and dict.get(key, None):   
        return dict[key]
    return None

@register.filter
def clean(val): 
    if val:   
        return val
    return ""

@register.filter
def field_value_exists(field, values):
    tags = field['tags']
    if tags and values:
        for t in tags: 
            if values.get(t, None):
                return True
    return False

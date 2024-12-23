from django import template

register = template.Library()

@register.filter
def repeat(value, times):
    """Repeat a string 'value' for 'times' times."""
    try:
        # Pastikan times adalah integer
        times = int(times)
        return value * times
    except (ValueError, TypeError):
        return ""
    
@register.filter
def rupiah(value):
    try:
        return "Rp {:,.0f}".format(value)  # Format number with commas and add Rp symbol
    except (ValueError, TypeError):
        return value


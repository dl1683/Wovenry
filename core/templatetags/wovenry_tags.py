from django import template

register = template.Library()


@register.filter
def visibility_icon(value):
    return "🔒" if value == "private" else "🌐"


@register.filter
def status_badge(value):
    if value == "draft":
        return "Draft"
    return "Published"

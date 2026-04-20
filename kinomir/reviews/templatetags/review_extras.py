from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter
def highlight(text, query):
    if not query or not text:
        return text
    escaped_query = re.escape(query)
    pattern = re.compile(f'({escaped_query})', re.IGNORECASE)
    highlighted = pattern.sub(r'<span class="highlight">\1</span>', str(text))
    return mark_safe(highlighted)
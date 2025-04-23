# cafe_app/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter
def format_price(value):
    return '{:,.0f}'.format(value)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), 1)  # مقدار پیش‌فرض ۱

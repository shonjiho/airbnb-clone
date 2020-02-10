from django import template

register = template.Library()


@register.filter(name="sexy_capital")
def weired_name(value):
    print(value)
    return "lalalla"

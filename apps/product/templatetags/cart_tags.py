from django import template
from apps.product.cart import Cart

register = template.Library()


def get_cart(context):
    request = context['request']
    return Cart(request.session)

register.assignment_tag(takes_context=True)(get_cart)

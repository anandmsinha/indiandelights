from django.shortcuts import render, get_object_or_404
from apps.home.models import Item
from jsonview.decorators import json_view
from django.views.decorators.http import require_POST
from .cart import Cart


def item_by_pk(request, pk):
    template_name = 'product/item.html'

    pk = long(pk)
    item = get_object_or_404(Item.objects.select_related('vendor__city', 'taste', 'unit'), pk=pk)
    return render(request, template_name, {'item': item})


@json_view
@require_POST
def cart_manager(request):
    post_data = request.POST
    error_reason = 'Type not specified'
    if 'type' in post_data:
        session_cart = Cart(request.session)
        query_type = post_data.get('type')
        error_reason = 'qtype does not exist - %s' % query_type
        if query_type == 'add':
            error_reason = 'product id and quantity not specified'
            if 'pid' in post_data and 'quantity' in post_data:
                product_id = long(post_data.get('pid'))
                product_qty = float(post_data.get('quantity'))
                product_item = Item.objects.select_related('unit').get(id=product_id)
                if product_item is not None:
                    session_cart.add(product_item, product_qty)
                    return {'success': True, 'cart': session_cart.cart_dict}
        elif query_type == 'remove':
            if 'pid' in post_data:
                product_id = long(post_data.get('pid'))
                product_item = Item.objects.get(id=product_id)
                session_cart.remove(product_item)
                return {'success': True, 'cart': session_cart.cart_dict}
        elif query_type == 'update':
            error_reason = 'products and quantity both are needed.'
            if 'products[]' in post_data and 'quantity[]' in post_data:
                products_list = post_data.getlist('products[]')
                quantity_list = post_data.getlist('quantity[]')
                error_reason = 'products and quantity both lists length should be same.'
                if len(products_list) !=0 and len(products_list) == len(quantity_list):
                    items_list = Item.objects.filter(pk__in=products_list).select_related('unit')
                    error_reason = 'products_list contains invalid ids.'
                    if len(items_list) == len(products_list):
                        filtered_qty = [float(qty) for qty in quantity_list]
                        for item, quantity in zip(items_list, filtered_qty):
                            session_cart.set_quantity(item, quantity)
                        return {'success': True, 'cart': session_cart.cart_dict}
    return {'success': False, 'reason': error_reason}, 400


def cart_view(request):
    template_name = 'product/cart.html'

    return render(request, template_name)

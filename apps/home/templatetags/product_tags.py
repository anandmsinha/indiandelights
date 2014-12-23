from django import template

register = template.Library()


def get_dropdown_qty(item):
    unit = item.unit
    op = ''
    if unit.weight:
        for i in range(1, 6):
            op = op + '<option value="%s">%s Kg</option>' % (i, i)
    elif unit.piece:
        for i in range(1, 6):
            op = op + '<option value="%s">%s Piece</option>' % (i, i)
    return op

register.simple_tag(get_dropdown_qty)
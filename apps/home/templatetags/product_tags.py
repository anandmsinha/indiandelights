from django import template

register = template.Library()


def get_dropdown_qty(item):
    unit = item.unit
    op = ''
    intunitval = int(item.unit.display_name.split()[0])
    if unit.weight:
        for i in range(1, 6):
            op = op + '<option value="%s">%s Kg</option>' % (i, i)
    elif unit.piece:
        for i in range(1, 6):
            op = op + '<option value="%s">%s Unit - %s pieces</option>' % (i, i, intunitval*i)
    return op

register.simple_tag(get_dropdown_qty)
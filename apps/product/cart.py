from decimal import Decimal
from json import loads, dumps


class CartItem(object):

    """
    class representing single instance of an cart item
    """

    def __init__(self, id, name, price, qty_display, qty,
                 thumbnail, lg_thumbnail):
        self.id = id
        self.name = name
        self.price = price
        self.qty_display = qty_display
        self.qty = qty
        self.thumbnail = thumbnail
        self.lg_thumbnail = lg_thumbnail
        self.total = float(self.price) * float(self.qty)

    def to_dict(self):
        return {
            'pk': self.id,
            'name': self.name,
            'price': self.price,
            'qty_display': self.qty_display,
            'qty': self.qty,
            'thumbnail': self.thumbnail,
            'lg_thumbnail': self.lg_thumbnail,
            'subtotal': self.total
        }

    @property
    def subtotal(self):
        total = float(self.price) * float(self.qty)
        logger.debug("cart item total - " + total)
        return total


class Cart(object):

    """
    for now the cart lives in session
    """

    def __init__(self, session):
        self._items_dict = {}
        self.session = session
        self.session_key = 'scart'
        if self.session_key in self.session:
            session_dict = loads(self.session[self.session_key])
            for k, v in session_dict.iteritems():
                self._items_dict[k] = CartItem(
                    v['pk'], v['name'], v['price'], v[
                        'qty_display'], v['qty'], v['thumbnail'],
                    v['lg_thumbnail'])

    def update_session(self):
        self.session[self.session_key] = self.cart_string
        self.session.modified = True

    def add(self, item, qty=1.0):
        qty = self.process_qty(qty)
        tmp_pk = str(item.pk)
        if tmp_pk in self._items_dict:
            self._items_dict[tmp_pk].qty += qty
        else:
            self._items_dict[tmp_pk] = CartItem(
                item.pk, item.name, item.price, item.unit.display_name, qty,
                item.image_small_thumbnail.url, item.image_thumbnail.url)
        self.update_session()

    def remove(self, item):
        tmp_pk = str(item.pk)
        if tmp_pk in self._items_dict:
            del self._items_dict[tmp_pk]
            self.update_session()
            return True
        return False

    def clear(self):
        self._items_dict = {}
        self.update_session()

    def process_qty(self, qty):
        qty = float(qty)
        if qty <= 0.0:
            raise ValueError('Quantity should be a positive number')
        return qty

    def set_quantity(self, item, qty):
        qty = self.process_qty(qty)
        item_pk = str(item.pk)
        if item_pk in self._items_dict:
            self._items_dict[item_pk].qty = qty
            self.update_session()
            return True
        return False

    @property
    def cart_string(self):
        return dumps(self.cart_dict)

    @property
    def cart_dict(self):
        output_dict = {}
        for k, v in self._items_dict.iteritems():
            output_dict[k] = v.to_dict()
        return output_dict

    @property
    def count(self):
        return len(self._items_dict)

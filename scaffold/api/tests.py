from api.models import Item
from django.db.utils import DataError, IntegrityError
from hypothesis import given
from hypothesis.extra.django import TestCase, from_model
from hypothesis.strategies import integers, just

# Create your tests here.


class ModelsTestCase(TestCase):
    @given(item=from_model(Item, id=just(None)))
    def test_create_item(self, item: Item):
        assert isinstance(item.name, str)
        assert item.stock >= 0
        assert item.sold >= 0

    @given(
        item=from_model(
            Item,
            id=just(None),
            create_time=just(None),
            update_time=just(None),
            last=just(None),
        ),
        quantity=integers(),
    )
    def test_item_buy(self, item: Item, quantity: int):
        assert isinstance(item.name, str)
        assert item.stock >= 0
        assert item.sold >= 0
        if quantity <= 0:  # quantity must large than 0
            self.assertRaises(DataError, item.buy, quantity)
        elif quantity > 2**31 - 1:  # quantity must not large than MAXINT
            self.assertRaises(DataError, item.buy, quantity)
        elif quantity > item.stock:  # quantity must not large than item stock
            self.assertRaises(IntegrityError, item.buy, quantity)
        else:
            stock = item.stock
            sold = item.sold
            item.buy(quantity)
            assert item.stock == (stock - quantity)
            assert item.sold == (sold + quantity)

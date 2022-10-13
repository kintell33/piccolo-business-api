from piccolo.table import Table
from piccolo.columns import Varchar, Float, ForeignKey, UUID, LazyTableReference, Timestamp
from piccolo.columns.m2m import M2M


class Business(Table):
    name = Varchar()
    logo = Varchar()

class Product(Table):
    name = Varchar()
    image = Varchar()
    price = Float()
    business = ForeignKey(Business)
    carts = M2M(LazyTableReference("CartProduct", module_path=__name__))

class Cart(Table):
    uuid = UUID()
    products = M2M(LazyTableReference("CartProduct", module_path=__name__))

class CartProduct(Table):
    cart = ForeignKey(Cart)
    product = ForeignKey(Product)

class Checkout(Table):
    cart = ForeignKey(Cart)
    total = Float()
    date = Timestamp()
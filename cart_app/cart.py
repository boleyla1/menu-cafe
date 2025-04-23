from cafe_app.models import Product
class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = product_qty
        self.session.modified = True

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        product_qty = self.cart
        return product_qty

    def delete(self, product):
        """حذف محصول از سبد خرید"""
        product_id = str(product)  # تبدیل به رشته برای کلید دیکشنری
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
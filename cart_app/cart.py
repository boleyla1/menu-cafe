from cafe_app.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(product.id): product for product in products}

        for product_id, quantity in self.cart.items():
            product = products_map.get(product_id)
            if product:
                total = product.price * int(quantity)
                yield {
                    'product': product,
                    'quantity': int(quantity),
                    'price': product.price,  # اضافه کردن price
                    'total': total,
                }

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] = int(self.cart[product_id]) + int(quantity)
        else:
            self.cart[product_id] = str(quantity)

        self.session.modified = True

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        return self.cart

    def total(self):
        return sum(item['total'] for item in self)

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

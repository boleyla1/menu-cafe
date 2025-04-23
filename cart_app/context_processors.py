from .cart import Cart


def cart_total(request):
    cart = Cart(request)
    total_quantity = sum(int(qty) for qty in cart.get_quants().values())  # جمع کل تعداد کالاها
    return {"cart_total_quantity": total_quantity}

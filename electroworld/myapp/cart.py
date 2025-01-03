# shop/cart.py

from django.shortcuts import get_object_or_404
from .models import Product  # Assuming your product model is named 'Product'

def get_cart(request):
    """
    Get the cart from session, or return an empty dictionary if not found.
    """
    cart = request.session.get('cart', {})
    return cart

def add_to_cart(request, product_id, quantity=1):
    """
    Adds a product to the cart.
    """
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] += quantity
    else:
        cart[str(product.id)] = {'quantity': quantity, 'price': product.price, 'name': product.name}

    request.session['cart'] = cart

def remove_from_cart(request, product_id):
    """
    Removes a product from the cart.
    """
    cart = get_cart(request)

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart

def update_cart(request, product_id, quantity):
    """
    Updates the quantity of a product in the cart.
    """
    cart = get_cart(request)

    if str(product_id) in cart:
        if quantity > 0:
            cart[str(product_id)]['quantity'] = quantity
        else:
            del cart[str(product_id)]

    request.session['cart'] = cart

def cart_total(cart):
    """
    Calculates the total price of the items in the cart.
    """
    total = 0
    for item in cart.values():
        total += item['price'] * item['quantity']
    return total

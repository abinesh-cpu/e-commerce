from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from .cart import add_to_cart, remove_from_cart, update_cart, get_cart, cart_total

# Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            return redirect(login)
        else:
            messages.error(request, 'Error in form submission. Please check your inputs.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login View
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect(index)  # Redirect to home page or any other page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Home Page View
def index(request):
    return render(request,'index.html')

def view_cart(request):
    """
    Displays the current items in the cart.
    """
    cart = get_cart(request)
    total_price = cart_total(cart)
    return render(request, 'shop/view_cart.html', {'cart': cart, 'total_price': total_price})

# Add to Cart
def add_to_cart_view(request, product_id):
    """
    Adds a product to the cart.
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        add_to_cart(request, product_id, quantity)
        return redirect('shop:view_cart')
    else:
        return HttpResponse(status=405)  # Method Not Allowed

# Remove from Cart
def remove_from_cart_view(request, product_id):
    """
    Removes a product from the cart.
    """
    remove_from_cart(request, product_id)
    return redirect('shop:view_cart')

# Edit Cart (Update Quantity)
def edit_cart_view(request, product_id):
    """
    Edits the quantity of a product in the cart.
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        update_cart(request, product_id, quantity)
        return redirect('shop:view_cart')
    else:
        return HttpResponse(status=405)  # Method Not 
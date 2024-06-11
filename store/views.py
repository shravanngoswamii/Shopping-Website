from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Sum
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after signup
            return redirect('home')  # Redirect to the home page after successful signup
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@csrf_protect
def user_logout(request):
    logout(request)
    return redirect('home')


# by myself
def home(request):
    categories = Category.objects.all()
    context = {'categories': categories, 'products': products,}
    return render(request, 'store/home.html', context)

def products(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category')
    products = Product.objects.all()
    
    if category:
        products = Product.objects.filter(category__name=category)
    
    categories = Category.objects.all()  # Retrieve all categories

    context = {
        'products': products,
        'selected_category': category,
        'search_query': search_query,
        'categories': categories,  # Pass the categories to the template
    }
    return render(request, 'store/products.html', context)



# by myself
def product_details(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'store/product_details.html', context)

from decimal import Decimal  # Import the Decimal data type for accurate currency calculations

from django.http import Http404

@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

        total_price = 0  # Initialize total_price

        # Calculate the total price with error handling for missing products
        for item in items:
            if item.product:
                total_price += item.calculate_total
            else:
                # Handle the case where the product is missing or deleted
                item.delete()  # Remove the invalid item from the cart

        categories = Category.objects.all()
        context = {'items': items, 'total_price': total_price, 'categories': categories}
    else:
        items = []
        total_price = 0
        context = {'items': items, 'total_price': total_price, 'categories': categories}

    return render(request, 'store/cart.html', context)


def update_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        new_quantity = int(request.POST.get("new_quantity"))

        # Update the cart based on your business logic here
        # Ensure to validate the quantity and check if the item is in the user's cart

        # Calculate the updated total price
        order_item = OrderItem.objects.get(id=item_id)

        if(new_quantity <= 0):
            order_item.delete()
        else:
            order_item.quantity = new_quantity
            order_item.save()

        # Recalculate the total price
        total_price = sum(item.calculate_total for item in order_item.order.orderitem_set.all())

        # Create a JSON response with the updated total_price and item_total
        response_data = {
            "total_price": total_price,
            "item_total": order_item.calculate_total,  # Add the individual item total
        }

        return JsonResponse(response_data)

    # Redirect back to the cart page or any other appropriate page
    return redirect('cart')




def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)

        # Get or create the user's cart
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            # Handle anonymous user cart (if needed)
            pass

        # Add the product to the cart (implement your logic)
        # For example, create an OrderItem for the product
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += 1
        order_item.save()

        return JsonResponse({"message": "Product added to the cart."})

    # Handle invalid requests
    return JsonResponse({"message": "Invalid request."}, status=400)




def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

        # Calculate the total price in the view
        total_price = sum(item.calculate_total for item in items)
        categories = Category.objects.all()
        context = {'items': items, 'total_price': total_price, 'categories': categories}
    else:
        items = []
        total_price = 0
        context = {'items': items, 'total_price': total_price, 'categories': categories}
    # context = {'items': items, 'total_price': total_price, 'categories': categories}
    return render(request, 'store/checkout.html', context)
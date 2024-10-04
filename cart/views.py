from django.shortcuts import render,get_object_or_404,redirect
from ecom.models import Product,CartItem,Cart,Order,Wish,WishItem
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm

def _cart_id(request):
    cart=request.user
    # print('you are',request.session.get('username'))
    if not cart:
        cart=request.user()
        print(f"Generated new cart ID: {cart}")
    cart.save()
    return cart

def add_cart(request,prd_id):
    product=Product.objects.get(id=prd_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart:cart_detail')

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            if cart_item.product.is_sale:
                price=cart_item.product.sale_price
            else:
                price=cart_item.product.price
            total+=(price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cartsum.html',dict(cart_items=cart_items,total=total,counter=counter))

def cart_remove(request,prd_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=prd_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request,prd_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=prd_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


def create_order(request,prd_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            current_user = request.user
            print(current_user)
            order = form.save(commit=False)
            # if current_user.is_staff and not current_user.is_superuser:
            order.customer = current_user
            product = Product.objects.get(pk=prd_id) 
            image = product.image
            order.image=image
            order.product = product

            order.save()
            full_remove(request,prd_id)
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form})

    

def myorder(request):
    ord=Order.objects.filter(customer=_cart_id(request))
    prd=Product.objects.filter
    return render(request, 'myorder.html',{'ord':ord})

def _wish_id(request):
    if request.user.is_authenticated:
        return Wish.objects.get_or_create(user=request.user)[0] 
    return None  



def add_wish(request, prd_id):
    product = get_object_or_404(Product, id=prd_id)
    wish, created = Wish.objects.get_or_create(user=request.user)
    
    wish_item, created = WishItem.objects.get_or_create(product=product, wish=wish)
    
    if created:
        wish_item.save()
    
    return redirect('cart:wish_detail')

def wish_detail(request):
    wish = get_object_or_404(Wish, user=request.user)
    wish_items = WishItem.objects.filter(wish=wish, active=True)
    return render(request, 'wishlist.html', {'wish_items': wish_items})

def remove_wish_item(request,prd_id):
    wish_item = get_object_or_404(Product, id=prd_id)
    wish_item.delete() #if you want to permanently remove it
    wish_item.save()
    return redirect('cart:wish_detail')

def combined_wish_cart(request, prd_id):
    add_cart(request, prd_id)
    wish_item = get_object_or_404(WishItem, product_id=prd_id, wish__user=request.user)
    # Remove the wish item
    wish_item.delete()  # Use delete if you want to permanently remove it
    # Redirect to the cart detail page
    return redirect('cart:cart_detail')


def create_order_for_all(request):
    if request.method == 'POST':
        current_user = request.user
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        form = OrderForm(request.POST)
        if form.is_valid():
        
            if cart_items.exists():
                for cart_item in cart_items:
                    product = cart_item.product
                    order = Order(
                    customer=current_user,
                    product=product,
                    quantity=cart_item.quantity,
                    image=product.image,
                    # Add any other fields necessary for the order
                )
                    order.save()
                # Optionally, remove the product from the cart after order creation
                    cart_item.delete()
        else:
            # Redirect to a confirmation page or home after placing all orders
            # return render('order.html')  
            form = OrderForm()
            return render(request, 'order.html', {'form': form})
        
    return redirect('cart:cart_detail')  # Redirect back to cart if the request is invalid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import CustomProduct

def get_or_create_cart(request):
    """Helper function to get or create a cart for the current user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    return cart

def cart_detail(request):
    """View for displaying the shopping cart"""
    cart = get_or_create_cart(request)
    
    context = {
        'cart': cart,
        'title': 'Your Shopping Cart - Magpie Crafts'
    }
    return render(request, 'cart/cart_detail.html', context)

@require_POST
def add_to_cart(request, product_id):
    """View for adding a product to the cart"""
    product = get_object_or_404(CustomProduct, id=product_id, is_public=True)
    cart = get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if product is already in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Updated quantity of {product.title} in your cart.')
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        messages.success(request, f'Added {product.title} to your cart.')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'cart_total': cart.total
        })
    
    return redirect('cart:cart_detail')

@require_POST
def update_cart(request, item_id):
    """View for updating cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    
    # Verify cart belongs to current user/session
    if (request.user.is_authenticated and cart.user == request.user) or \
       (not request.user.is_authenticated and cart.session_id == request.session.session_key):
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'cart_total': cart.total,
            'item_subtotal': cart_item.subtotal if quantity > 0 else 0
        })
    
    return redirect('cart:cart_detail')

@require_POST
def remove_from_cart(request, item_id):
    """View for removing an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    
    # Verify cart belongs to current user/session
    if (request.user.is_authenticated and cart.user == request.user) or \
       (not request.user.is_authenticated and cart.session_id == request.session.session_key):
        
        product_title = cart_item.product.title
        cart_item.delete()
        messages.success(request, f'Removed {product_title} from your cart.')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'cart_total': cart.total
        })
    
    return redirect('cart:cart_detail')

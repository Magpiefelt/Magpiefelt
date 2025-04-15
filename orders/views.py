from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe
import json

from .models import Order, OrderItem
from cart.models import Cart
from products.models import CustomProduct

# Initialize Stripe API
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """View for the checkout page"""
    # Get the current cart
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart = Cart.objects.filter(session_id=session_id).first()
    
    if not cart or not cart.items.exists():
        messages.warning(request, 'Your cart is empty. Please add some products before checkout.')
        return redirect('cart:cart_detail')
    
    # Calculate totals
    subtotal = cart.total
    gst = round(subtotal * 0.05, 2)  # 5% GST for Canada
    shipping_cost = 0  # Will be calculated based on shipping method
    total = subtotal + shipping_cost  # GST is included in product prices
    
    context = {
        'cart': cart,
        'subtotal': subtotal,
        'gst': gst,
        'shipping_cost': shipping_cost,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'title': 'Checkout - Magpie Crafts'
    }
    return render(request, 'orders/checkout.html', context)

def create_payment_intent(request):
    """Create a Stripe Payment Intent"""
    try:
        data = json.loads(request.body)
        
        # Get the current cart
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_id = request.session.session_key
            cart = Cart.objects.filter(session_id=session_id).first()
        
        if not cart or not cart.items.exists():
            return JsonResponse({'error': 'Your cart is empty'}, status=400)
        
        # Calculate totals
        subtotal = cart.total
        shipping_cost = 0  # Will be calculated based on shipping method
        total = subtotal + shipping_cost
        
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Convert to cents
            currency='cad',
            metadata={
                'cart_id': cart.id,
                'user_id': request.user.id if request.user.is_authenticated else None,
            },
        )
        
        return JsonResponse({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def place_order(request):
    """Process the order after successful payment"""
    if request.method != 'POST':
        return redirect('orders:checkout')
    
    # Get the current cart
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        cart = Cart.objects.filter(session_id=session_id).first()
    
    if not cart or not cart.items.exists():
        messages.warning(request, 'Your cart is empty. Please add some products before checkout.')
        return redirect('cart:cart_detail')
    
    # Get form data
    payment_intent_id = request.POST.get('payment_intent_id')
    
    # Create order
    order = Order(
        user=request.user if request.user.is_authenticated else None,
        email=request.POST.get('email'),
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name'),
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        province=request.POST.get('province'),
        postal_code=request.POST.get('postal_code'),
        phone=request.POST.get('phone'),
        stripe_payment_intent_id=payment_intent_id,
        stripe_payment_status='succeeded',
        subtotal=cart.total,
        gst=round(cart.total * 0.05, 2),  # 5% GST for Canada
        shipping_cost=0,  # Will be calculated based on shipping method
        total=cart.total,  # Total including shipping
        shipping_method=request.POST.get('shipping_method', 'Standard Shipping'),
        customer_notes=request.POST.get('customer_notes', '')
    )
    order.save()
    
    # Create order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            product_name=cart_item.product.title,
            product_price=cart_item.product.price.incl_tax,
            quantity=cart_item.quantity
        )
        
        # Update product inventory (if implemented)
        # product = cart_item.product
        # product.stock -= cart_item.quantity
        # product.save()
    
    # Clear the cart
    cart.items.all().delete()
    
    # Send order confirmation email (to be implemented)
    # send_order_confirmation_email(order)
    
    messages.success(request, 'Your order has been placed successfully! Thank you for shopping with Magpie Crafts.')
    return redirect('orders:order_confirmation', order_id=order.id)

def order_confirmation(request, order_id):
    """Display order confirmation page"""
    order = get_object_or_404(Order, id=order_id)
    
    # Security check - only allow the user who placed the order to view it
    if request.user.is_authenticated and order.user and order.user != request.user:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('products:product_list')
    
    context = {
        'order': order,
        'title': 'Order Confirmation - Magpie Crafts'
    }
    return render(request, 'orders/order_confirmation.html', context)

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'error': str(e)}, status=400)
    
    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        handle_successful_payment(payment_intent)
    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object
        handle_failed_payment(payment_intent)
    
    return JsonResponse({'status': 'success'})

def handle_successful_payment(payment_intent):
    """Handle successful payment webhook event"""
    # Update order status if it exists
    order = Order.objects.filter(stripe_payment_intent_id=payment_intent.id).first()
    if order:
        order.stripe_payment_status = 'succeeded'
        order.status = 'processing'
        order.save()

def handle_failed_payment(payment_intent):
    """Handle failed payment webhook event"""
    # Update order status if it exists
    order = Order.objects.filter(stripe_payment_intent_id=payment_intent.id).first()
    if order:
        order.stripe_payment_status = 'failed'
        order.status = 'cancelled'
        order.save()

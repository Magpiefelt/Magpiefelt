from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'subtotal']
    fields = ['product', 'product_name', 'product_price', 'quantity', 'subtotal']
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'email', 'city', 'province', 'created_at', 'status', 'total', 'actions']
    list_filter = ['status', 'created_at', 'province']
    search_fields = ['first_name', 'last_name', 'email', 'address', 'city']
    readonly_fields = ['stripe_payment_intent_id', 'stripe_payment_status', 'created_at', 'updated_at', 'subtotal', 'gst', 'shipping_cost', 'total']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': (('first_name', 'last_name'), 'email', 'phone')
        }),
        ('Shipping Information', {
            'fields': ('address', ('city', 'province', 'postal_code'), 'shipping_method', 'tracking_number')
        }),
        ('Order Details', {
            'fields': (('subtotal', 'gst'), ('shipping_cost', 'total'), 'status')
        }),
        ('Payment Information', {
            'fields': ('stripe_payment_intent_id', 'stripe_payment_status'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Customer'
    
    def actions(self, obj):
        if obj.status == 'processing':
            mark_shipped_url = reverse('admin:mark_order_shipped', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" style="background-color: #28a745; color: white;">Mark Shipped</a>',
                mark_shipped_url
            )
        elif obj.status == 'shipped' and not obj.tracking_number:
            add_tracking_url = reverse('admin:add_tracking_number', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" style="background-color: #17a2b8; color: white;">Add Tracking</a>',
                add_tracking_url
            )
        return ""
    actions.short_description = 'Actions'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                'mark-shipped/<int:order_id>/',
                self.admin_site.admin_view(self.mark_order_shipped),
                name='mark_order_shipped',
            ),
            path(
                'add-tracking/<int:order_id>/',
                self.admin_site.admin_view(self.add_tracking_number),
                name='add_tracking_number',
            ),
        ]
        return custom_urls + urls
    
    def mark_order_shipped(self, request, order_id):
        from django.shortcuts import redirect
        from django.contrib import messages
        
        order = Order.objects.get(id=order_id)
        order.status = 'shipped'
        order.save()
        
        messages.success(request, f'Order #{order.id} has been marked as shipped.')
        return redirect('admin:orders_order_change', order_id)
    
    def add_tracking_number(self, request, order_id):
        from django.shortcuts import render, redirect
        from django.contrib import messages
        from django import forms
        
        class TrackingForm(forms.Form):
            tracking_number = forms.CharField(max_length=100, required=True)
        
        order = Order.objects.get(id=order_id)
        
        if request.method == 'POST':
            form = TrackingForm(request.POST)
            if form.is_valid():
                order.tracking_number = form.cleaned_data['tracking_number']
                order.save()
                messages.success(request, f'Tracking number added to order #{order.id}.')
                return redirect('admin:orders_order_change', order_id)
        else:
            form = TrackingForm()
        
        context = {
            'title': f'Add Tracking Number to Order #{order.id}',
            'form': form,
            'order': order,
            'opts': self.model._meta,
        }
        return render(request, 'admin/orders/add_tracking.html', context)

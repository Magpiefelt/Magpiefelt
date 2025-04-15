from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from .models import ProductCategory, CustomProduct

def product_list(request):
    """View for displaying all products"""
    categories = ProductCategory.objects.all()
    products = CustomProduct.objects.filter(is_public=True)
    
    # Filter by product type if specified
    product_type = request.GET.get('type')
    if product_type and product_type in dict(CustomProduct.PRODUCT_TYPE_CHOICES):
        products = products.filter(product_type=product_type)
        type_display = dict(CustomProduct.PRODUCT_TYPE_CHOICES)[product_type]
        title = f"{type_display} - Magpie Crafts"
    else:
        title = "All Products - Magpie Crafts"
    
    context = {
        'categories': categories,
        'products': products,
        'title': title,
        'product_types': CustomProduct.PRODUCT_TYPE_CHOICES
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    """View for displaying a single product"""
    product = get_object_or_404(CustomProduct, slug=slug, is_public=True)
    
    # Get related products (same category or product type)
    related_products = CustomProduct.objects.filter(
        is_public=True
    ).exclude(id=product.id)
    
    if product.categories.exists():
        related_products = related_products.filter(
            categories__in=product.categories.all()
        )[:4]
    else:
        related_products = related_products.filter(
            product_type=product.product_type
        )[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'title': f"{product.title} - Magpie Crafts"
    }
    return render(request, 'products/product_detail.html', context)

def category_detail(request, slug):
    """View for displaying products filtered by category"""
    category = get_object_or_404(ProductCategory, slug=slug)
    products = CustomProduct.objects.filter(
        categories=category,
        is_public=True
    )
    
    context = {
        'category': category,
        'products': products,
        'title': f"{category.name} - Magpie Crafts"
    }
    return render(request, 'products/category_detail.html', context)

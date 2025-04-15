from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from oscar.apps.catalogue.abstract_models import AbstractProduct

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Product Categories'
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class CustomProduct(AbstractProduct):
    """
    Extension of Oscar's AbstractProduct to add custom fields for wool felting products
    """
    PRODUCT_TYPE_CHOICES = (
        ('kit', 'Felting Kit'),
        ('art', 'Felted Art'),
        ('candy', 'Vegan Candy'),
        ('bundle', 'Bundle'),
    )
    
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default='kit')
    difficulty_level = models.CharField(max_length=20, blank=True, null=True)
    time_to_complete = models.CharField(max_length=50, blank=True, null=True)
    materials_included = models.TextField(blank=True, null=True)
    techniques_used = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def get_product_type_display_name(self):
        return dict(self.PRODUCT_TYPE_CHOICES)[self.product_type]

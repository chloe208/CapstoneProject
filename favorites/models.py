from django.db import models

# Create your models here.
from products.models import Product, ProductImage

class Favorite(models.Model):
    products = models.ManyToManyField(Product, null=True, blank=True)
    productimage = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.00) # DELETE THIS
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.id

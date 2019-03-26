from django.urls import reverse
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models
from django import forms

from PIL import Image
from io import BytesIO

import sys, os


# Create your models here.
# THE WAY TO DESIGN YOUR DATABASE
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique =True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'catogories'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=120, null=False)
    title = models.CharField(max_length=120, null=False)
    name = models.CharField(max_length=120, null=False)
    brand = models.CharField(max_length=120, null=False)
    makeup_type = models.CharField(max_length=120)
    vegan = models.BooleanField(default=False) 
    description = models.TextField()
    how_to_use = models.TextField()
    # inventory
    quantity = models.IntegerField()
    out_of_stock = models.BooleanField(default=False)
    # COLOR RECOGNITION
    hexa = models.CharField(max_length=120)
    rgb = models.CharField(max_length=120)
    # PRICING
    price = models.DecimalField(decimal_places=2, max_digits=100, default=29.99)
    sale_price = models.DecimalField(decimal_places=2, max_digits=100,
                                     null=True, blank=True)
    #image = models.FileField(upload_to='products/images/', null=True)
    #Slug will never change by putting 'unique' inside the parenthesis.
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # to make sure title and slug are unique
    class Meta:
        unique_together = ('title', 'slug')

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse("single_product", args=[self.slug])
        # return reverse("single_product", kwargs={"slug":self.slug})

# additional image for the product


class ProductImage(models.Model):
    name = models.CharField(max_length=10)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")
    # def save(self):
    #     #Opening the uploaded image
    #     im = Image.open(self.image).convert('RGB')
    #     output = BytesIO()
    #     #Resize/modify the image
    #     im = im.resize( (300,300) )
    #     #after modifications, save it to the output
    #     im.save(output, format='JPEG' or 'PNG', quality=100)
    #     output.seek(0)
    #     #change the imagefield value to be the newley modifed image value
    #     self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" or "%s.png" %self.image.name.split('.')[0], 'image/jpeg' or 'image/png', sys.getsizeof(output), None)
    #     super(ProductImage,self).save()
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    # FOR ACTIVE -- if there is a picture coming up, set to false
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    def __str__(self):
        return self.name

    
RATINGS = (
        ('⭐⭐⭐⭐⭐', '5'),
        ('⭐⭐⭐⭐', '4'),
        ('⭐⭐⭐', '3'),
        ('⭐⭐', '2'),
        ('⭐', '1')
)
class Comment(models.Model):
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    ratings = models.CharField(max_length=120, default='★★★★★', choices=RATINGS)
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approved(self):
        self.approved = True
        self.save()

    def __str__(self):
        return str(self.product)


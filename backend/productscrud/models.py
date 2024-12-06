from django.db import models

# Create your models here.

class Tags(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.FloatField(null=True, blank=True)
    stock = models.IntegerField()
    tags = models.ManyToManyField(Tags, related_name="products", blank=True)
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    weight = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    depth = models.FloatField()
    warranty_information = models.CharField(max_length=255)
    shipping_information = models.CharField(max_length=255)
    availability_status = models.CharField(max_length=50)
    return_policy = models.CharField(max_length=255)
    minimum_order_quantity = models.IntegerField()
    images = models.JSONField(default=list, blank=True)
    thumbnail = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    barcode = models.BigIntegerField()
    qr_code = models.URLField()

class Review(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    reviewer_name = models.CharField(max_length=100)
    reviewer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)   
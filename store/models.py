from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null = True)
    email = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null = True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True) # pip install pillow

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True) # auto_now_add=True means that the date will be added automatically
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null = True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True) # on_delete=models.SET_NULL means that if the product is deleted, the order will still be there
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True) # on_delete=models.SET_NULL means that if the order is deleted, the product will still be there
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True) # auto_now_add=True means that the date will be added automatically

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) # on_delete=models.SET_NULL means that if the customer is deleted, the shipping address will still be there
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True) # on_delete=models.SET_NULL means that if the order is deleted, the shipping address will still be there
    address = models.CharField(max_length=200, null = True)
    city = models.CharField(max_length=200, null = True)
    state = models.CharField(max_length=200, null = True)
    zipcode = models.CharField(max_length=200, null = True)
    date_added = models.DateTimeField(auto_now_add=True) # auto_now_add=True means that the date will be added automatically

    def __str__(self):
        return self.address
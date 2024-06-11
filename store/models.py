from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model

# Create your models here.
   
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.full_name
    

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

 
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url   

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) #if customer is deleted, set to null
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null = True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all() #set of all items in order
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all() #set of all items in order
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all() #set of all items in order
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)  # if product is deleted, set to null
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)  # if order is deleted, set to null
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def calculate_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) #if customer is deleted, set to null
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True) #if order is deleted, set to null
    address = models.CharField(max_length=200, null = False)
    city = models.CharField(max_length=200, null = False)
    state = models.CharField(max_length=200, null = False)
    zipcode = models.CharField(max_length=200, null = False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
    
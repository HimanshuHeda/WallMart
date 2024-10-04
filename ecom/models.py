from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser,PermissionsMixin
# Create your models here.


# Model for category
class Category(models.Model):
    name=models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_images/', blank=False, null=True)
    def __str__(self):
        return self.name
    


# Models for customer
genderchoices = [
    ('male', "Male"),
    ('female', "Female"),
]
class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    gender= models.CharField(max_length=100,choices=genderchoices,default='male')
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=10)
    # password=models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
# models for products
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(default=0, decimal_places=2,max_digits=10)
    category=models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
    description=models.CharField(max_length=250,blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=False, null=True)
    stock = models.IntegerField(default=0)
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0, decimal_places=2,max_digits=10)



    def __str__(self):
        return self.name
    




    
class User(AbstractUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    #gender= models.CharField(max_length=100,choices=genderchoices,default='male')
    email=models.EmailField(max_length=50,unique=True)
    # phone=models.CharField(max_length=11)

    is_staff = models.BooleanField(default=True)



class Order(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='order_images/', blank=False, null=True)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=100,default='',blank=False)
    phone=models.CharField(max_length=10,default='' ,blank=False)
    date=models.DateField(default=datetime.datetime.today)
    paymentstatus=models.BooleanField(default=True)
    deliverydate=models.DateField(null=True)
    placedorder=models.BooleanField(default=True)
    shipped=models.BooleanField(default=False)
    delivery=models.BooleanField(default=False)


    def __str__(self):
        return f'{self.product} {self.customer}'

class Cart(models.Model):
    cart_id=models.ForeignKey(User,on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='Cart'
        ordering=['date_added']
    def __str__(self):
         return '{}'.format(self.cart_id)
class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)
    class Meta:
        db_table='CartItem'
    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return '{}'.format(self.product)
    
class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Change this to 'user'
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Wish'
        ordering = ['date_added']

    def __str__(self):
        return '{}'.format(self.user)  # Change this accordingly
class WishItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    wish=models.ForeignKey(Wish,on_delete=models.CASCADE)
    # quantity=models.IntegerField()
    active=models.BooleanField(default=True)
    class Meta:
        db_table='WishItem'
    # def sub_total(self):
    #     return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} in {self.wish}"
    



from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ShoppingCart(models.Model):
    pass

class Client(models.Model):
    client_name = models.CharField(max_length=255)
    client_surname = models.CharField(max_length=255)
    client_email = models.CharField(max_length=255)
    client_phonenumber = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE, null = True, blank=True)

    def __str__(self):
        return self.client_name + ' ' + self.client_surname


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=255)
    employee_surname = models.CharField(max_length=255)

    def __str__(self):
        return self.employee_name + ' ' + self.employee_surname


class Product(models.Model):
    price = models.FloatField()
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255)
    product_category = models.CharField(max_length=255, null = True, blank = True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/', null = True, blank=True)
    def __str__(self):
        return self.product_name

class ProductShoppingcart(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ShoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    def __str__(self):
        return self.Product.product_name + ' ' + str(self.ShoppingCart.id)

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_price = models.FloatField()
    date_created = models.DateField()

    def __str__(self):
        return self.client.user.username

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.product_name + ' ' + str(self.order.id)
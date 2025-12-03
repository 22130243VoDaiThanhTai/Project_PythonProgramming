from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    userID = models.IntegerField(default=0)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

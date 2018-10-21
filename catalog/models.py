from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=100)


class  Product(models.Model):
	name = models.CharField(max_length=100)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product")
	brand = models.CharField(max_length=100)
	nutrition_grade = models.CharField(max_length=1)
	picture = models.UrlField()
	url = models.UrlFirld()


class UserFavorite(models.Model):
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
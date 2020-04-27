from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	user 			= models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name 			= models.CharField(max_length=45, null=True)
	email 			= models.CharField(max_length=45, null=True)
	phone 			= models.CharField(max_length=45, null=True)
	profile_pic 	= models.ImageField(default="default.png", null=True, blank=True)
	date_created 	= models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=45, null=True)
	def __str__(self):
		return self.name

class Product(models.Model):

	CATEGORY = (
		('In door', 'In door'),
		('Out door', 'Out door'),
	)
	tag 			= models.ManyToManyField(Tag)
	name 			= models.CharField(max_length=45, null=True)
	price 			= models.FloatField(null=True)
	category 		= models.CharField(max_length=45, null=True, choices=CATEGORY)
	description 	= models.CharField(max_length=45, null=True)
	date_created 	= models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Order(models.Model):

	STATUS = (
		('Pending', 'Pending'),
		('Out of delievery', 'Out of delievery'),
		('Delieverd', 'Delieverd'),
	)

	# models.SET_NULL // When customer delete the customer relation set to null
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

	status = models.CharField(max_length=45, choices=STATUS)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.name
		
		

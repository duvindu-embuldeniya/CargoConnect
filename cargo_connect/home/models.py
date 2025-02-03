from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile', null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True, default='+94 12 12345')

    def __str__(self):
        return f"{self.user.username}'s profile"
	
    @property
    def imageURL(self):
        try: 
            url = self.image.url
        except:
            url = '/images/profile/default.png'
        return url 
    

class Product(models.Model):

	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 
	
	by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True) 
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	delivery_address = models.TextField()
	note = models.CharField(max_length=100, null=True, blank=True)
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['-date_created']


class Order(models.Model):
	STATUS = (
			('Delivered', 'Delivered'),
			('In Transit', 'In Transit'),
			) 

	customer = models.ForeignKey(User, on_delete= models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete= models.CASCADE, null=True)
	date_created = models.DateTimeField(default=timezone.now)
	note = models.CharField(max_length=100, null=True, blank=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return str(self.product)
	
	class Meta:
		ordering = ['-date_created']




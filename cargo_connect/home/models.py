from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True, default='+94 12 12345')
    email = models.EmailField(null = True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_profile = Profile.objects.get(pk=self.pk)
            old_image = old_profile.image if old_profile.image else None
        else:
            old_image = None

        super(Profile, self).save(*args, **kwargs)

        #New image uploaded, delete the old one
        if self.image and self.image != old_image:
            if old_image:
                try:
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path)
                except Exception as e:
                    print(f"Error deleting old image: {e}")

        #Image removed, delete the current image
        elif not self.image and old_image:
            try:
                # Delete the current image from the filesystem
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)
            except Exception as e:
                print(f"Error deleting current image: {e}")

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
            img.close()


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





from django.db import models
from datetime import datetime
from cloudinary.models import CloudinaryField
import random
import string


def generate_tracking_id():
    # Generate 3 random alphabets
    alphabets = ''.join(random.choice(string.ascii_letters) for _ in range(3))
    
    # Generate 6 random digits
    numbers = ''.join(random.choice(string.digits) for _ in range(6))
    
    # Combine alphabets and numbers
    tracking_id = alphabets + numbers
    
    return tracking_id


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Product(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'ACTIVE'),
        ('UNAVAILABLE', 'UNAVAILABLE')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    tracking_id = models.CharField(max_length=255, default="nil")
    current_location = models.CharField(max_length=255, default="nil")
    quantity = models.CharField(max_length=255, default="nil")
    brand = models.CharField(max_length=255, default="nil")
    sub_category = models.CharField(max_length=255, default="nil")
    status = models.CharField(choices=STATUS_CHOICES, max_length=17, default='ACTIVE')

    price = models.DecimalField(max_digits=10, decimal_places=2)
    countdown_time = models.DurationField()
    image = CloudinaryField("image", default="https://cdn1.iconfinder.com/data/icons/technology-devices-2/100/Profile-512.png")
    image2 = CloudinaryField("image", default="https://cdn1.iconfinder.com/data/icons/technology-devices-2/100/Profile-512.png")
    image3 = CloudinaryField("image", default="https://cdn1.iconfinder.com/data/icons/technology-devices-2/100/Profile-512.png")
    image4 = CloudinaryField("image", default="https://cdn1.iconfinder.com/data/icons/technology-devices-2/100/Profile-512.png")
    image5 = CloudinaryField("image", default="https://cdn1.iconfinder.com/data/icons/technology-devices-2/100/Profile-512.png")
    timestamp = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name



class PremiumProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    countdown_time = models.DurationField()
    image = CloudinaryField("image", default="https://cdn1.iconfinder.com/data/icons/technology-devices-2/100/Profile-512.png")
    extra_feature = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return self.name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete')
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='giftweb',)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    premium_product = models.ForeignKey(PremiumProduct, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=100, blank=True, default='')
    payment_id = models.CharField(max_length=100, blank=True, default=generate_tracking_id)

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    country = models.CharField(max_length=255, default="nil")

    full_name = models.CharField(max_length=255, default="nil")
    street_address = models.CharField(max_length=200, default="nil")
    apartment_address = models.CharField(max_length=200, default="nil")
    phone_number = models.CharField(max_length=200, default="nil")

    proof_of_pay = CloudinaryField("image", default="https://cdn1.iconfinder.com/data/icons/technology-devices-2/100/Profile-512.png")
    gift_card_type = models.CharField(choices=[('apple', 'Apple Card'), ('amazon', 'Amazon Card'), ('steam', 'Steam Card'), ('xbox', 'Xbox Card')], max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    def mark_as_complete(self):
        self.completed = True
        self.save()
    def __str__(self):
        return f"{self.user} paid {self.amount} for {self.product}"

    class Meta:
        verbose_name = "Manage Deposit/Payment"
        verbose_name_plural = "Manage Deposit/Payment"


class CartItem(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    premium_product = models.ForeignKey(PremiumProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart item {self.id} - User: {self.user.username}, Product: {self.product.name}"

class Blog(models.Model):
    topic = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/')
    body = models.CharField(max_length=255)
    date = models.DateField()
    read_more = models.CharField(max_length=255, default='GiftCard')

    def __str__(self):
        return self.topic

class Contactor(models.Model):
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=100)
  subject = models.CharField(max_length=200, blank=True)

  message = models.TextField(blank=True)
  contact_date = models.DateTimeField(default=datetime.now, blank=True)
  user_id = models.IntegerField(blank=True)


  def __str__(self):
    return self.name



class Notification(models.Model):    
  name = models.CharField(max_length=200)
  user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notify',)
  image = CloudinaryField("image", default="")
  subject = models.CharField(max_length=200, blank=True)
  message = models.TextField(blank=True)
  contact_date = models.DateTimeField(default=datetime.now, blank=True)


  def __str__(self):
    return self.name
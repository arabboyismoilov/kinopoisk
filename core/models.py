from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class CustomUser(AbstractUser):
    class ROLE_TYPE(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
        
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(choices=ROLE_TYPE, default=ROLE_TYPE.USER)
    REQUIRED_FIELDS = ['role']
    
class Movie(models.Model):
    class PAYMENT_TYPE(models.TextChoices):
        BEPUL = 'bepul', 'Bepul'
        OBUNA = 'obuna', 'Obuna'
        
    
    class MOVIE_TYPE(models.TextChoices):
        KINO = 'kino', 'Kino'
        SERIAL = 'serial', 'Serial'
        SERIAL_QISM = 'serial_qism', 'Serial Qism'
    
        
    nomi = models.CharField(max_length=300)
    payment_turi = models.CharField(choices=PAYMENT_TYPE, default=PAYMENT_TYPE.OBUNA)
    info = models.TextField()
    rating = models.FloatField(null=True)
    yil = models.IntegerField()
    janr = models.CharField()
    treyler_youtube_url = models.CharField(null=True)
    treyler= models.FileField(upload_to='treylers', null=True)
    movie_type = models.CharField(choices=MOVIE_TYPE, default=MOVIE_TYPE.KINO)
    serial_qism_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to='thumbnails')
    rejisyor = models.CharField(blank=True)
    aktyorlar = models.CharField(blank=True)
    sifati = models.CharField(blank=True)
    tillar = models.CharField(blank=True)
    video = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Payment(models.Model):
    class PROVIDER_TYPE(models.TextChoices):
        CLICK = 'click', 'Click'
        PAYME = 'payme', 'Payme'
        UZUM = 'uzum', 'Uzum'
    
    
    amount = models.DecimalField(decimal_places=2, max_digits=19)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    provider_type = models.CharField(choices=PROVIDER_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class Subscription(models.Model):
    class TYPE(models.TextChoices):
        OYLIK = 'oylik', 'Oylik'
        YILLIK = 'yillik', 'Yillik'
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(default=datetime.now())
    end_date = models.DateTimeField()
    type = models.CharField(choices=TYPE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
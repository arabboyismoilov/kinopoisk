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
    
    
class MovieVideo(models.Model):
    title = models.CharField()
    file = models.FileField(upload_to='movies/')
    created_at = models.DateTimeField(auto_now_add=True)


class MovieTreyler(models.Model):
    title = models.CharField()
    file = models.FileField(upload_to='treylers/')
    created_at = models.DateTimeField(auto_now_add=True)
    

class MovieThubmnail(models.Model):
    title = models.CharField()
    file = models.FileField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    
    
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
    treyler= models.ForeignKey(MovieTreyler, on_delete=models.SET_NULL, null=True)
    movie_type = models.CharField(choices=MOVIE_TYPE, default=MOVIE_TYPE.KINO)
    serial_qism_number = models.IntegerField(null=True)
    thumbnail = models.ForeignKey(MovieThubmnail, on_delete=models.SET_NULL, null=True)
    rejisyor = models.CharField(blank=True)
    aktyorlar = models.CharField(blank=True)
    sifati = models.CharField(blank=True)
    tillar = models.CharField(blank=True)
    video = models.ForeignKey(MovieVideo, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    class TYPE(models.TextChoices):
        OYLIK = 'oylik', 'Oylik'
        YILLIK = 'yillik', 'Yillik'
    type = models.CharField(choices=TYPE)
    price = models.DecimalField(decimal_places=2, max_digits=19)
    duration = models.IntegerField(default=31) # in days
    
    created_at = models.DateTimeField(auto_now_add=True)
    

class UserSubscription(models.Model):
    class Status(models.TextChoices):
        NOT_PAID = 'not_paid', 'Not Paid'
        PAID = 'paid', 'Paid'
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_subscribtions')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=19)
    status = models.CharField(choices=Status, default=Status.NOT_PAID)
    start_date = models.DateTimeField(default=datetime.now())
    end_date = models.DateTimeField()    
    created_at = models.DateTimeField(auto_now_add=True)
        
    
    

class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = 'created', 'Created'
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=19)
    status = models.CharField(choices=Status, default=Status.CREATED)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class Payment(models.Model):
    class PROVIDER_TYPE(models.TextChoices):
        CLICK = 'click', 'Click'
        PAYME = 'payme', 'Payme'
        UZUM = 'uzum', 'Uzum'
    
    amount = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    provider_transaction_id = models.CharField()
    provider_type = models.CharField(choices=PROVIDER_TYPE)
    create_time = models.BigIntegerField() # unix system time
    perform_time = models.BigIntegerField(null=True)
    state = models.IntegerField()
    reason = models.IntegerField(null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

class VerificationOTP(models.Model):
    phone = models.CharField()
    code = models.CharField()
    expire_date = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
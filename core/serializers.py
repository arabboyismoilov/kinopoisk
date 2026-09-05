from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from core.models import Movie, Subscription, Payment, Order, UserSubscription, VerificationOTP, MovieVideo

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'created_at']
        read_only_fields = ['id', 'created_at']
        
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }
        
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'nomi',
            'payment_turi',
            'info',
            'rating',
            'yil',
            'janr',
            'treyler_youtube_url',
            'treyler',
            'movie_type',
            'serial_qism_number',
            'thumbnail',
            'rejisyor',
            'aktyorlar',
            'sifati',
            'tillar',
            'video'
        ]
    
    

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'nomi',
            'payment_turi',
            'info',
            'rating',
            'yil',
            'janr',
            'treyler_youtube_url',
            'treyler',
            'movie_type',
            'serial_qism_number',
            'thumbnail',
            'rejisyor',
            'aktyorlar',
            'sifati',
            'tillar'
        ]
        

class MovieDetailSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField(source="video__file.url")
    class Meta:
        model = Movie
        fields = [
            'nomi',
            'payment_turi',
            'info',
            'rating',
            'yil',
            'janr',
            'treyler_youtube_url',
            'treyler',
            'movie_type',
            'serial_qism_number',
            'thumbnail',
            'rejisyor',
            'aktyorlar',
            'sifati',
            'tillar',
            'video_url'
        ]

    def get_video_url(self, obj):
        return obj.video.file.url

class OrderUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']    


class SubscritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'type', 'price', 'duration', 'created_at']
        read_only_fields = ['id', 'created_at']


class OrderUserSubscription(serializers.ModelSerializer):
    subscription = SubscritionSerializer(read_only=True)
    class Meta:
        model = UserSubscription
        fields = ['id', 'price', 'status', 'start_date', 'end_date', 'subscription']


class OrderCreateSerializer(serializers.ModelSerializer):
    subscription_id = serializers.PrimaryKeyRelatedField(queryset = Subscription.objects.all(), write_only=True)
    user_subscription = OrderUserSubscription(read_only=True)
    user = OrderUser(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'subscription_id', 'user_subscription', 'user', 'amount', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'status', 'amount']
    
    def create(self, validated_data):
        user = validated_data['user']
        subscription = validated_data['subscription_id']
        end_date = datetime.now() + timedelta(days=subscription.duration)
        
        us = UserSubscription.objects.create(user=user, subscription=subscription, price=subscription.price, end_date=end_date)
        return Order.objects.create(user=user, user_subscription=us, amount=subscription.price)
    
    
class PaymeApiRequestSerializer(serializers.Serializer):
    method = serializers.CharField()
    params = serializers.DictField()
    

class MovieVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieVideo
        fields = ['id', 'title', 'file', 'created_at']
        read_only_fields = ['id', 'created_at']
    
        
        
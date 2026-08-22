from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import Movie, Subscription, Payment

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
        

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'amount', 'provider_type', 'id', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        
class SubscriptionSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer()
    class Meta:
        model = Subscription
        fields = [
            'id', 'start_date', 'end_date', 'type', 'payment'
        ]
        
    def create(self, validated_data):
        user = validated_data.get('user')
        payment_data = validated_data.pop('payment')
        payment = Payment.objects.create(**payment_data, user = user)
        return Subscription.objects.create(**validated_data, payment = payment)
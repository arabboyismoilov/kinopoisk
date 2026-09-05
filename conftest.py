# fixture
import pytest
from rest_framework.test import APIClient
from core.models import CustomUser, Movie, Subscription, UserSubscription
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta, timezone

@pytest.fixture
def api_client():
    return APIClient()
    


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username='ali', password='1234')

@pytest.fixture
def user2():
    return CustomUser.objects.create_user(username='ali2', password='1234')


@pytest.fixture
def jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return refresh.access_token


@pytest.fixture
def jwt_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    token = refresh.access_token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def mock_client(api_client, user):
    api_client.force_authenticate(user)
    return api_client



@pytest.fixture(autouse=True)
def movies(db):
    sample_video = SimpleUploadedFile(
        name="sample",
        content=b"salom",
        content_type="video/mp4"
    )
    
    sample_image = SimpleUploadedFile(
        name="sample",
        content=b"salom",
        content_type="image/jpeg"
    )
    
    Movie.objects.create(
        nomi="avatar",
        payment_turi = 'bepul',
        info = 'Yaxshi kino',
        yil = 2012,
        janr = "Action",
        movie_type = "kino",
        thumbnail = sample_image,
        video = sample_video,
    )
    
    Movie.objects.create(
        nomi="avatar 2",
        payment_turi = 'obuna',
        info = 'Yaxshi kino',
        yil = 2014,
        janr = "Action",
        movie_type = "kino",
        thumbnail = sample_image,
        video = sample_video,
    )


@pytest.fixture(autouse=True)
def subscriptions(db, user):
    oylik = Subscription.objects.create(type='oylik', price=24000)
    Subscription.objects.create(type='yillik', price=199000, duration=365)
    
    UserSubscription.objects.create(user=user, subscription=oylik, price=oylik.price, status='paid', start_date = datetime.now(timezone.utc) - timedelta(days=1), end_date=datetime.now(timezone.utc) + timedelta(days=31))
    
    
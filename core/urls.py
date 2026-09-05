from django.urls import path


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from core import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/register', views.RegisterView.as_view(), name='register'),
    path('api/movie', views.MovieListCreateApiView.as_view(), name='movie'),
    path('api/movie/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail'),
    path('api/subscription', views.SubscriptionListCreateView.as_view(), name='subscription'),
    path('api/orders', views.OrderListCreateView.as_view(), name='order'),
    path('api/checkout-url/<int:orderId>', views.CheckoutUrlCreateApiView.as_view(), name='checkout'),
    path('api/payme', views.PaymeMerchantApiView.as_view(), name='payme'),
    path('api/send-otp/<slug:phone>', views.OTPSendApiView.as_view(), name='otp-send'),
    path('api/verify-otp<slug:phone>/<slug:code>', views.OtpVerificationAPIView.as_view(), name='verify-send'),
    path('api/movie-videos', views.MovieVideoApiView.as_view(), name='movie-videos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core import serializers
from rest_framework.permissions import IsAuthenticated, BasePermission
from core.models import CustomUser, Movie, Subscription, Payment
from datetime import datetime

def has_active_subscription(user: CustomUser):
    subscription = user.subscriptions.filter(end_date__gte = datetime.now())
    if subscription:
        return True
    return False

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == CustomUser.ROLE_TYPE.ADMIN


class CanWatch(BasePermission):
    message = "User has not subcription"
    
    def has_object_permission(self, request, view, obj):
        if obj.payment_turi == Movie.PAYMENT_TYPE.BEPUL:
            return True
        if has_active_subscription(request.user):
            return True
        return False


class RegisterView(CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    

class MovieListCreateApiView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = serializers.MovieCreateSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated(), IsAdmin()]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.MovieListSerializer
        return super().get_serializer_class()
    

class MovieDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MovieCreateSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), CanWatch()]
        return [IsAuthenticated(), IsAdmin()]    
    
    
class SubscritionListCreateApiView(ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
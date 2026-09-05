from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core import serializers
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from core.models import CustomUser, Movie, Subscription, Payment, Order, UserSubscription, VerificationOTP, MovieVideo
from datetime import datetime, timezone, timedelta
from django.conf import settings
import base64
from core.authentications import PaymeBasicAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from core.exeptions import PaymeInvalidRequestException, PaymeOrderInvalidAmountException, PaymeOrderNotFoundException
from time import time
import logging
import core.utils as utils
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers as rest_serializer

logger = logging.getLogger(__name__) # core.views

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == CustomUser.ROLE_TYPE.ADMIN


class CanWatch(BasePermission):
    message = "User has not subcription"
    
    def has_object_permission(self, request, view, obj):
        if obj.payment_turi == Movie.PAYMENT_TYPE.BEPUL:
            return True
        
        if request.user.user_subscribtions.filter(start_date__lte=datetime.now(timezone.utc), end_date__gte = datetime.now(timezone.utc), status='paid').exists():
            return True
        return False


class RegisterView(CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    
    def perform_create(self, serializer):
        
        logger.info("username %s is registered", serializer.validated_data['username'])
        return super().perform_create(serializer)
    

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
    serializer_class = serializers.MovieDetailSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), CanWatch()]
        return [IsAuthenticated(), IsAdmin()]    
    


class SubscriptionListCreateView(ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = serializers.SubscritionSerializer


    
class OrderListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class CheckoutUrlCreateApiView(APIView):
    def post(self, request, orderId):
        logger.info(f"{request.user.id} created checkout link for order {orderId}")
        order = Order.objects.get(id=orderId)
        amount = int(order.amount*100)
        base_checkout_url = settings.PAYME_CHECKOUT_URL
        merchant_id = settings.PAYME_MERCHANT_ID
        data = f"m={merchant_id};ac.order_id={orderId};a={amount}"
        encoded = base64.b64encode(data.encode("utf-8"))
        b64_string = encoded.decode("utf-8")
        return Response(
            data={
                "checkout_url": f"{base_checkout_url}/{b64_string}"
            }
        )
        
from time import sleep
class PaymeMerchantApiView(APIView):
    authentication_classes = [PaymeBasicAuthentication]
    def post(self, request):
        serializer = serializers.PaymeApiRequestSerializer(data=request.data)
        if not serializer.is_valid():
            raise PaymeInvalidRequestException(data=serializer.errors)
        
        data = serializer.validated_data
        method = data['method']
        params = data['params']
        
        if method == 'CheckPerformTransaction':
            amount = params['amount']
            order_id = params['account']['order_id']
            logger.debug("Checkperofrm trasction method keldi rderId[%s] userid[%s]", order_id, request.user.id)
            
            
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                raise PaymeOrderNotFoundException()
            
            order_amount = int(order.amount*100)
            if order_amount != amount:
                raise PaymeOrderInvalidAmountException()
            
            
            response = Response(
                data = {
                    "result": {
                        "allow": True
                    }
                }
            )
            logger.debug("Checkperofrm trasction method ketdi rderId[%s] userid[%s]", order_id, request.user.id)
            
        elif method == 'CreateTransaction':
            
            payme_transaction_id = params['id']
            create_time = params['time']
            amount = params['amount']
            order_id = params['account']['order_id']
            
            order = Order.objects.get(id=order_id)
            
            payment = Payment.objects.create(
                user=order.user, 
                provider_transaction_id=payme_transaction_id, 
                provider_type=Payment.PROVIDER_TYPE.PAYME,
                amount = amount,
                create_time = create_time,
                state = 1,
                order=order
            )
            
            order.status = Order.Status.PENDING
            order.save()
            
            response = Response(
                data = {
                    "result": {
                        "create_time": create_time,
                        "transaction": f"{payment.id}",
                        "state": 1
                    }
                }
            )
        elif method == 'PerformTransaction':
            provider_trasnaction_id = params['id']
            payment = Payment.objects.get(provider_transaction_id=provider_trasnaction_id)
            payment.perform_time = time()*1000
            payment.state = 2
            payment.save()
            
            order = payment.order
            order.status = Order.Status.COMPLETED
            order.save()
            
            user_subscription = order.user_subscription
            user_subscription.status = UserSubscription.Status.PAID
            user_subscription.save()
            
            response = Response(
                data = {
                    "result": {
                        "transaction": f"{payment.id}",
                        "perform_time": payment.perform_time,
                        "state": 2
                    },
                    "id": 3
                }
            )
        return response
    

@extend_schema(
    tags=['OTP Auth'],
    responses={
        200: inline_serializer(
            name='Success',
            fields={
                'status': rest_serializer.CharField()
            }
        )
    }
)
class OTPSendApiView(APIView):
    def post(self, request, phone):
        veriication_otp, created = VerificationOTP.objects.get_or_create(
            phone=phone, 
            defaults={
                "code": utils.generate_random_code(),
                "expire_date": datetime.now(timezone.utc) + timedelta(minutes=30)
            }
        )
        
        if created:
            print(f"Sizni tasdqilash kodingiz: {veriication_otp.code}")
            
            user = CustomUser(username=phone)
            user.set_unusable_password()
            user.save()
        
            return Response(
                data={
                    "status": "sent"
                }
            )
            
        if not created:
            now = datetime.now(timezone.utc)
            if veriication_otp.expire_date <= now or veriication_otp.used or veriication_otp.created_at < now - timedelta(minutes=1):
                veriication_otp.code = utils.generate_random_code()
                veriication_otp.expire_date = now + timedelta(minutes=30)
                veriication_otp.used = False
                veriication_otp.save()
                print(f"Sizni tasdqilash kodingiz: {veriication_otp.code}")
                return Response(
                    data={
                        "status": "sent"
                    }
                )
                
        
        return Response(
                data={
                    "status": "exists"
                }
            )
        
@extend_schema(
    tags=['OTP Auth'],
    responses={
        200: inline_serializer(
            name="Success",
            fields={
                "refresh": rest_serializer.CharField()
            }         
        )
    }
)
class OtpVerificationAPIView(APIView):
    def post(self, request, phone, code):
        try:
            otp = VerificationOTP.objects.get(phone=phone)
        except VerificationOTP.DoesNotExist:
            raise NotFound(detail="Code for this phone not found")
        
        
        now = datetime.now(timezone.utc)
        print(otp.expire_date, otp.code, otp.used)
        
        if otp.expire_date < now or otp.used:
            raise ValidationError(detail="Expired or used", code="NOT_VALID")
        
        if otp.code != code:
            raise ValidationError(detail="Incorret code", code="INCORRECT_CODE")
        
        try:
            user = CustomUser.objects.get(username=phone)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found for this phone")
        
        refresh = RefreshToken.for_user(user)
        otp.used = True
        otp.save()
            
        return Response(
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        )
        
    

class MovieVideoApiView(ListCreateAPIView):
    serializer_class = serializers.MovieVideoSerializer
    queryset = MovieVideo.objects.all()
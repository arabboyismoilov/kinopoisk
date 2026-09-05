from rest_framework.authentication import BaseAuthentication
import base64
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class PaymeClient:
    def __init__(self):
        self.name = 'Payme'
        self.is_authenticated = True


class PaymeBasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        type, encoded = header.split(" ")
        if type != 'Basic':
            return None
        
        try:    
            creds = base64.b64decode(encoded).decode('utf-8') # username:parol
        except Exception:
            raise AuthenticationFailed(detail="Invaliud base64")
        
        username, parol = creds.split(":")
        
        if username != settings.PAYME_USERNAME or parol != settings.PAYME_PAROL:
            raise AuthenticationFailed(detail="Invalid creds")
        
        return (PaymeClient(), None)
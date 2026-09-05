from rest_framework.exceptions import APIException


class PaymeApiException(APIException):
    status_code = 200
    def __init__(self, code: int, message_en: str, message_uz: str = "", message_ru: str = "", data=None):
        self.detail = {
            "error": {
                "code": code,
                "message": {
                    "uz": message_uz,
                    "ru": message_ru,
                    "en": message_en
                },
            }
        }
        if data:
            self.detail['error']['data'] = data
        super().__init__(self.detail)
        
        
class PaymeInvalidRequestException(PaymeApiException):
    def __init__(self, data=None):
        super().__init__(code=-32600, message_en="Invalid request", data=data)
        

class PaymeOrderNotFoundException(PaymeApiException):
    def __init__(self, data=None):
        super().__init__(code=-31050, message_en="Order not found", data=data)
        

class PaymeOrderInvalidAmountException(PaymeApiException):
    def __init__(self, data=None):
        super().__init__(code=-31001, message_en="Order amount not correct", data=data)
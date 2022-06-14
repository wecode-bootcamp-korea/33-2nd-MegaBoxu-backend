import jwt
from django.http import JsonResponse
from django.conf import settings
from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
            
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"},print(access_token), status = 400)

    return wrapper

import jwt, requests

from django.http import JsonResponse
from django.conf import settings
from django.views import View

from users.models import User

class KakaoLoginView(View):
    def get(self, request):
        code = request.GET.get('code')
        KAKAO_TOKEN_API = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type'  : 'authorization_code',
            'redirect_uri': 'http://localhost:3000/users/kakao/callback',
            'client_id'   : settings.KAKAO_APPKEY,
            'code'        : code
        }
        access_token   = requests.post(KAKAO_TOKEN_API, data=data).json()['access_token']

        KAKAO_INFO_API = 'https://kapi.kakao.com/v2/user/me'
        user_info      = requests.get(KAKAO_INFO_API, headers={'Authorization': f'Bearer {access_token}'}).json()
        kakao_id       = user_info['id']
        name           = user_info['properties']['name']
        email          = user_info['kakao_account']['email']
        phone_number   = user_info['kakao_account']['phone_number']

        user, is_created = User.objects.get_or_create(
            kakao_id=kakao_id,
            defaults={
                'name' : name,
                'email': email,
                'phone_number' : phone_number
            }
        )

        status       = 201 if is_created else 200
        message      = 'FIRSTLOGIN' if is_created else 'LOGIN'
        mega_token = jwt.encode({'id':user.id}, settings.SECRET_KEY, settings.ALGORITHM)
        print(mega_token)
        return JsonResponse({'message': message, 'token': mega_token}, status=status)
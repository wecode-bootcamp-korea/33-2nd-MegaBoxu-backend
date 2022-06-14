import jwt, requests

from django.http import JsonResponse
from django.conf import settings
from django.views import View

from users.models import User

class KakaoLoginView(View):
    def get(self, request):
        try:
            kakao_token_api = "https://kauth.kakao.com/oauth/token"
            data = {
                "grant_type"  : "authorization_code",
                "client_id"   : settings.KAKAO_APPKEY,
                "redirect_uri": "http://localhost:3000/users/kakao/callback",
                "code"        : request.GET.get("code")
            }

            access_token = requests.post(kakao_token_api, data=data, timeout = 1).json().get('access_token')
            user_info    = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f"Bearer {access_token}"}, timeout = 1).json()
            kakao_id          = user_info["id"]
            kakao_name        = user_info["properties"]["nickname"]
            kakao_email       = user_info["kakao_account"]["email"]
            profile_image_url = user_info["properties"]["profile_image"]    # 프로필 기능 구현 하게 될 것 대비

            user, is_created = User.objects.get_or_create(
                defaults = {
                    "kakao_id"     : kakao_id,
                    "name"         : kakao_name,
                    "email"        : kakao_email
                    # "profile_image": profile_image_url    프로필 설정 모델링 변경하게 되면 추가하기. 
                }
            )
            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
 
            if is_created:
                return JsonResponse({"message" : "ACCOUNT CREATED", "token" : access_token}, status=201)
                
            else:
                return JsonResponse({"message" : "SIGN IN SUCCESS", "token" : access_token}, status=200)
            
        except KeyError:
            return JsonResponse({'message' : "KEY_ERROR"}, status=400)

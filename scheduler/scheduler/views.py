from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from rest_auth.registration.views import SocialLoginView


# Todo: SocialLoginView 따라 들어가면 get_social_login이라는 뷰가 있음. 추후 커스터마이징에 이용
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter


class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
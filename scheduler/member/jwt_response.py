from .models import UserProfile
from .serializers import UserProfileSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    user_profile = UserProfile.objects.get(user_id=user.id)

    user_info = UserProfileSerializer(user_profile).data
    user_info['token'] = token

    return {
        'user_info': user_info
    }

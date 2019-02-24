from django.utils import timezone

from django.db.models import Q

from .models import UserProfile, User, FriendRequest

from .serializers import UserProfileSerializer, FriendRequestSerializer

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action


class UserProfileViewSet(viewsets.GenericViewSet,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'status': 201,
                'message': '회원가입 성공'
            }, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response({
                'status': 500,
                'message': '회원가입 오류'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response({
                'status': 201,
                'message': '정보 수정 성공'
            }, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'status': 500,
                'message': '정보 수정 오류'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False)
    def search(self, request):
        try:
            user = request.GET.get('name')
            user = UserProfile.objects.get(user__nickname=user)

            user_data = {
                'email': user.user.email,
                'username': user.user.username,
                'nickname': user.user.nickname,
                'birth': user.birth,
            }

            return Response({
                'status': 200,
                'user': user_data,
            })
        except:
            return Response({
                'status': 200,
                'message': '유저를 찾을 수 없습니다'
            })


class FriendRequestViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def create(self, request, *args, **kwargs):
        try:
            friend_request = FriendRequest.objects.get(Q(request_user=request.data['response_user'], response_user=request.data['request_user'])
                                                       | Q(request_user=request.data['request_user'], response_user=request.data['response_user']))
            if friend_request.assent:
                return Response({
                    'status': 200,
                    'message': '이미 친구 상태'
                })

            if friend_request.request_user.id == int(request.data['request_user']):
                return Response({
                    'status': 200,
                    'message': '이미 친구 요청을 보냄'
                })
            else:
                friend_request.assent = True
                friend_request.assented_at = timezone.now()
                friend_request.save()

                request_user = UserProfile.objects.get(user__id=int(request.data['request_user']))
                response_user = UserProfile.objects.get(user_id=int(request.data['response_user']))

                req_user = User.objects.get(id=request_user.user_id)
                res_user = User.objects.get(id=response_user.user_id)

                request_user.friends.add(res_user)
                request_user.save()
                response_user.friends.add(req_user)
                response_user.save()

                return Response({
                    'status': 200,
                    'message': '친구 요청 수락',
                })
        except:
            if request.data['request_user'] == request.data['response_user']:
                return Response({
                    'status': 200,
                    'message': '자기 자신에게는 친구 요청 불가'
                })

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response({
                'status': 201,
                'message': '친구 요청 보냄'
            }, status=status.HTTP_201_CREATED, headers=headers)
from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import Schedule, Holiday
from .serializers import ScheduleSerializer, ScheduleCreateSerializer, HolidaySerializer
from .permissions import IsOwner

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class ScheduleViewSet(viewsets.GenericViewSet,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Schedule.objects.all()
    permission_classes = (IsAuthenticated, IsOwner, )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScheduleSerializer
        else:
            return ScheduleCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        schedule = serializer.save()

        registrant = serializer.validated_data['registrant']
        schedule.participants.add(registrant)
        schedule.save()

        headers = self.get_success_headers(serializer.data)
        return Response({
            'status': 201,
            'message': '일정 생성 완료'
        }, status=status.HTTP_201_CREATED, headers=headers)

    # Todo: invite action 뷰 생성 (fcm 활용)

    @action(detail=True, methods=['GET'])
    def join(self, request, pk=None):
        try:
            participant_id = request.GET.get('id')
            participant = User.objects.get(pk=participant_id)
            Schedule.objects.get(pk=pk, participants=participant)
            return Response({
                'success': False,
                'data': {
                    'message': '일정에 이미 참가 중인 유저'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'data': {
                    'message': '일정에 추가할 user_id를 다시 확인해주세요.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except Schedule.DoesNotExist:
            instance = self.get_object()
            instance.participants.add(participant)

            return Response({
                'success': True,
                'data': {
                    'message': '일정에 user 추가'
                }
            }, status=status.HTTP_200_OK)
        except ValueError:
            return Response({
                'success': False,
                'data': {
                    'message': '요청 형식에 맞지 않습니다.'
                }
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET'])
    def leave(self, request, pk=None):
        try:
            participant_id = request.GET.get('id')
            schedule = Schedule.objects.get(pk=pk)

            if not schedule.participants.filter(pk=participant_id).exists():
                return Response({
                    'success': False,
                    'data': {
                        'message': '해당 일정에 참가하고 있지 않습니다.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            participant = User.objects.get(pk=participant_id)
            if participant.id == schedule.registrant_id:
                schedule.delete()

                return Response({
                    'success': True,
                    'data': {
                        'message': '일정 삭제 완료'
                    }
                }, status=status.HTTP_200_OK)
            else:
                schedule.participants.remove(participant)

                return Response({
                    'success': True,
                    'data': {
                        'message': '일정 나가기 완료'
                    }
                }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'data': {
                    'message': '해당 유저를 찾을 수 없습니다.'
                }
            }, status=status.HTTP_404_NOT_FOUND)
        except Schedule.DoesNotExist:
            return Response({
                'success': False,
                'data': {
                    'message': '해당 일정을 찾을 수 없습니다.'
                }
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'success': False,
                'data': {
                    'message': '요청 형식에 맞지 않습니다.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def expulsion(self, request, pk=None):
        try:
            obj = Schedule.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)

            user = request.GET.get('id')
            if not obj.participants.filter(pk=user).exists():
                return Response({
                    'success': True,
                    'data': {
                        'message': '해당 일정에 참가하고 있지 않습니다.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(pk=user)
            if obj.registrant_id == user.pk:
                return Response({
                    'success': False,
                    'data': {
                        'message': '일정 등록자는 추방시킬 수 없습니다.'
                    }
                })
            else:
                obj.participants.remove(user)
                return Response({
                    'success': True,
                    'data': {
                        'user': user.pk,
                        'message': '해당 유저 일정에서 추방 완료'
                    }
                }, status=status.HTTP_200_OK)
        except Schedule.DoesNotExist:
            return Response({
                'success': False,
                'data': {
                    'message': '해당 일정을 찾을 수 없습니다.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'data': {
                    'message': '해당 유저를 찾을 수 없습니다.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({
                'success': False,
                'data': {
                    'message': '요청 형식에 맞지 않습니다.'
                }
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET'])
    def arrival(self, request, pk=None):
        try:
            user = request.GET.get('id')
            instance = Schedule.objects.get(pk=pk)

            if instance.arrival_member.filter(pk=user).exists():
                return Response({
                    'success': False,
                    'data': {
                        'message': '이미 도착한 유저입니다.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            if instance.participants.filter(pk=user).exists():
                user = User.objects.get(pk=user)
                instance.arrival_member.add(user)

                return Response({
                    'success': True,
                    'data': {
                        'user': user.pk,
                        'message': '도착 완료'
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'data': {
                        'message': '해당 일정에 참가하고 있지 않습니다.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
        except Schedule.DoesNotExist:
            return Response({
                'success': False,
                'data': {
                    'message': '해당 일정을 찾을 수 없습니다.'
                }
            }, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'data': {
                    'message': '해당 유저를 찾을 수 없습니다.'
                }
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'sucess': False,
                'data': {
                    'message': '요청 형식에 맞지 않습니다.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def filter(self, request):
        user_id = request.GET.get('id')
        schedules = Schedule.objects.filter(participants=user_id)

        if schedules:
            serializer = ScheduleSerializer(schedules, many=True)

            return Response({
                "success": True,
                "data": {
                    "schedules": serializer.data
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": True,
                "data": {
                    "message": "참여 중인 일정이 없습니다."
                }
            }, status=status.HTTP_200_OK)


class HolidayViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Holiday.objects.filter(is_holiday=True)
    serializer_class = HolidaySerializer

    def list(self, request, *args, **kwargs):
        year = request.GET.get('year')

        queryset = self.filter_queryset(self.get_queryset())
        if year:
            queryset = queryset.filter(date__year=year)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
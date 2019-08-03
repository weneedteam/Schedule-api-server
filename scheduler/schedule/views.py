from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import Schedule, Holiday
from .serializers import ScheduleSerializer, ScheduleCreateSerializer, HolidaySerializer
from .permissions import IsOwner
from . import exceptions

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
            'success': True,
            'data': {
                'schedule': serializer.data
            }
        }, status=status.HTTP_201_CREATED, headers=headers)

    # Todo: invite action 뷰 생성 (fcm 활용)

    @action(detail=True, methods=['GET'])
    def join(self, request, pk=None):
        try:
            participant_id = request.GET.get('id')
            participant = User.objects.get(pk=participant_id)
            Schedule.objects.get(pk=pk, participants=participant)

            raise exceptions.ScheduleUserAlreadyExistsException
        except User.DoesNotExist:
            raise exceptions.UserNotFoundException
        except Schedule.DoesNotExist:
            instance = self.get_object()
            instance.participants.add(participant)

            return Response({
                'success': True,
                'data': {
                    'user_id': participant.pk,
                    'message': '일정에 유저 추가 완료',
                }
            }, status=status.HTTP_200_OK)
        except ValueError:
            raise exceptions.RequestFormatException

    @action(detail=True, methods=['GET'])
    def leave(self, request, pk=None):
        try:
            participant_id = request.user.pk
            schedule = Schedule.objects.get(pk=pk)

            if not schedule.participants.filter(pk=participant_id).exists():
                raise exceptions.ScheduleNotParticipantException

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
                        'user_id': participant.pk,
                        'message': '일정 나가기 완료'
                    }
                }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise exceptions.UserNotFoundException
        except Schedule.DoesNotExist:
            raise exceptions.ScheduleNotFoundException

    @action(detail=True, methods=['POST'])
    def expulsion(self, request, pk=None):
        try:
            obj = Schedule.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)

            user = User.objects.get(pk=request.GET.get('id'))
            if not obj.participants.filter(pk=user.id).exists():
                raise exceptions.ScheduleNotParticipantException

            if obj.registrant == user:
                raise exceptions.ScheduleExpulsionPermissionException
            else:
                obj.participants.remove(user)

                return Response({
                    'success': True,
                    'data': {
                        'user_id': user.pk,
                        'message': '해당 유저 일정에서 추방 완료'
                    }
                }, status=status.HTTP_200_OK)
        except Schedule.DoesNotExist:
            raise exceptions.ScheduleNotFoundException
        except User.DoesNotExist:
            raise exceptions.UserNotFoundException
        except ValueError:
            raise exceptions.RequestFormatException

    @action(detail=True, methods=['GET'])
    def arrival(self, request, pk=None):
        try:
            user = request.user
            instance = Schedule.objects.get(pk=pk)

            if instance.arrival_member.filter(pk=user.pk).exists():
                raise exceptions.ScheduleUserAlreadyArrivalException

            if instance.participants.filter(pk=user.pk).exists():
                instance.arrival_member.add(user)

                return Response({
                    'success': True,
                    'data': {
                        'user_id': user.pk,
                        'message': '일정 도착 완료'
                    }
                }, status=status.HTTP_200_OK)
            else:
                raise exceptions.ScheduleNotParticipantException
        except Schedule.DoesNotExist:
            raise exceptions.ScheduleNotFoundException
        except User.DoesNotExist:
            raise exceptions.UserNotFoundException

    @action(detail=False, methods=['GET'])
    def filter(self, request):
        user_id = request.GET.get('id')
        schedules = Schedule.objects.filter(participants=user_id)

        if schedules:
            serializer = ScheduleSerializer(schedules, many=True)

            return Response({
                'success': True,
                'data': {
                    'message': '참여하고 있는 일정 불러오기 완료',
                    'schedules': serializer.data
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': True,
                'data': {
                    'message': '참여 중인 일정이 없습니다.'
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

        return Response({
            'success': True,
            'data': {
                'message': '휴일 리스트 불러오기 완료',
                'holidays': serializer.data
            }
        }, status=status.HTTP_200_OK)

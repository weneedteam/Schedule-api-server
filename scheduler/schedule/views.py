from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import Schedule, Holiday
from .serializers import ScheduleSerializer, HolidaySerializer

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response


User = get_user_model()

class ScheduleViewSet(viewsets.GenericViewSet,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

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
        participant_id = request.GET.get('id')
        try:
            participant = User.objects.get(pk=participant_id)
            Schedule.objects.get(pk=pk, participants=participant)
            return Response({
                'status': 200,
                'message': '일정에 이미 참가 중인 유저',
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'status': 400,
                'message': '일정에 추가할 user의 id를 입력해주세요',
            }, status=status.HTTP_200_OK)
        except Schedule.DoesNotExist:
            instance = self.get_object()
            instance.participants.add(participant)

            return Response({
                'status': 200,
                'message': '일정에 user 추가',
            }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def leave(self, request, pk=None):
        schedule = Schedule.objects.get(pk=pk)
        participant_id = request.GET.get('id')
        try:
            try:
                Schedule.objects.get(pk=pk, participants=participant_id)
            except Schedule.DoesNotExist:
                return Response({
                    'success': False,
                    'data': {
                        'message': '해당 일정에 참가하고 있지 않습니다.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
            participant = User.objects.get(pk=participant_id)
            if participant.id == schedule.registrant_id:
                Schedule.objects.filter(pk=pk).delete()

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
            }, status=status.HTTP_400_BAD_REQUEST)
        except Schedule.DoesNotExist:
            return Response({
                'success': False,
                'data': {
                    'message': '해당 일정을 찾을 수 없습니다.'
                }
            })


class HolidayViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Holiday.objects.all().filter(is_holiday=True)
    serializer_class = HolidaySerializer

    @action(detail=False, methods=['GET'])
    def filter(self, request):
        year = request.GET.get('year')
        holidays = Holiday.objects.all().filter(is_holiday=True, date__year=year)
        serializer = HolidaySerializer(holidays, many=True)

        return Response(serializer.data)
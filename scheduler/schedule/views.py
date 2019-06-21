from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import Schedule, Holiday
from .serializers import ScheduleSerializer, ScheduleCreateSerializer, HolidaySerializer
from .permissions import IsOwner
from . import responses

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

        response = responses.ScheduleCreateSuccess
        response['data']['schedule'] = serializer.data

        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    # Todo: invite action 뷰 생성 (fcm 활용)

    @action(detail=True, methods=['GET'])
    def join(self, request, pk=None):
        try:
            participant_id = request.GET.get('id')
            participant = User.objects.get(pk=participant_id)
            Schedule.objects.get(pk=pk, participants=participant)

            response = responses.ScheduleUserAlreadyExistsError

            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            response = responses.UserNotFoundError
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Schedule.DoesNotExist:
            instance = self.get_object()
            instance.participants.add(participant)

            response = responses.ScheduleInviteSuccess
            response['data']['user'] = participant.pk

            return Response(response, status=status.HTTP_200_OK)
        except ValueError:
            response = responses.RequestFormatError

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def leave(self, request, pk=None):
        try:
            participant_id = request.GET.get('id')
            schedule = Schedule.objects.get(pk=pk)

            if not schedule.participants.filter(pk=participant_id).exists():
                response = responses.ScheduleNotParticipantedError

                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            participant = User.objects.get(pk=participant_id)
            if participant.id == schedule.registrant_id:
                schedule.delete()
                response = responses.ScheduleDeleteSuccess

                return Response(response, status=status.HTTP_200_OK)
            else:
                schedule.participants.remove(participant)

                response = responses.ScheduleLeaveSuccess
                response['data']['user'] = participant.pk

                return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            response = responses.UserNotFoundError

            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Schedule.DoesNotExist:
            response = responses.ScheduleNotFoundError

            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            response = responses.RequestFormatError

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def expulsion(self, request, pk=None):
        try:
            obj = Schedule.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)

            user = request.GET.get('id')
            if not obj.participants.filter(pk=user).exists():
                response = responses.ScheduleNotParticipantedError

                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(pk=user)
            if obj.registrant_id == user.pk:
                response = responses.ScheduleExpulsionPermissionError

                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                obj.participants.remove(user)
                response = responses.ScheduleExpulsionSuccess
                response.data['user'] = user.pk

                return Response(response, status=status.HTTP_200_OK)
        except Schedule.DoesNotExist:
            response = responses.ScheduleNotFoundError

            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            response = responses.UserNotFoundError

            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            response = responses.RequestFormatError

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def arrival(self, request, pk=None):
        try:
            user = request.GET.get('id')
            instance = Schedule.objects.get(pk=pk)

            if instance.arrival_member.filter(pk=user).exists():
                response = responses.ScheduleUserAlreadyArrivalError

                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if instance.participants.filter(pk=user).exists():
                user = User.objects.get(pk=user)
                instance.arrival_member.add(user)

                response = responses.ScheduleArrivalSuccess
                response['data']['user'] = user.pk

                return Response(response, status=status.HTTP_200_OK)
            else:
                response = responses.ScheduleNotParticipantedError

                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Schedule.DoesNotExist:
            response = responses.ScheduleNotFoundError

            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            response = responses.UserNotFoundError

            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            response = responses.RequestFormatError

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def filter(self, request):
        user_id = request.GET.get('id')
        schedules = Schedule.objects.filter(participants=user_id)

        if schedules:
            serializer = ScheduleSerializer(schedules, many=True)

            response = responses.ScheduleFilterListSuccess
            response['data']['schedules'] = serializer.data

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = responses.ScheduleFilterEmptySuccess

            return Response(response, status=status.HTTP_200_OK)


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

        response = responses.HolidayListSuccess
        response['data']['holidays'] = serializer.data

        return Response(response, status=status.HTTP_200_OK)
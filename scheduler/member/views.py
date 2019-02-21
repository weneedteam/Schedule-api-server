from django.shortcuts import render

from .models import UserProfile, User

from .serializers import UserProfileSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response


class UserProfileViewSet(viewsets.ModelViewSet):
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
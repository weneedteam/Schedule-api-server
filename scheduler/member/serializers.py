from rest_framework import serializers

from .models import UserProfile, User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'nickname', )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'nickname', 'password', 'password2', )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('패스워드가 일치하지 않습니다')
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = UserProfile
        fields = ('user', 'birth', 'language', )

    def update(self, instance, validated_data):
        user_data = validated_data['user']
        user = User.objects.get(id=instance.user_id)
        UserSerializer.update(UserSerializer(), instance=user, validated_data=user_data)

        instance.birth = validated_data.get('birth', instance.birth)
        instance.language = validated_data.get('language', instance.language)
        instance.save()

        return instance


class UserProfileCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=True)
    class Meta:
        model = UserProfile
        fields = ('user', 'birth', 'language', )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserCreateSerializer.create(UserCreateSerializer(), validated_data=user_data)
        user_profile = UserProfile.objects.create(user=user, birth=validated_data['birth'], language=validated_data['language'])

        return user_profile


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('request_user', 'response_user', )


class EmailValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', )


class NicknameValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname', )
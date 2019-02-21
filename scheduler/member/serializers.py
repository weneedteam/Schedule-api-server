from rest_framework import serializers

from .models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(max_length=128)
    class Meta:
        model = User
        fields = ('email', 'username', 'nickname', 'password')

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError("Password deosn't match.")
    #
    # return cd['password2']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = UserProfile
        fields = ('user', 'birth', 'language', )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user_profile = UserProfile.objects.create(user=user, birth=validated_data.pop('birth'), language=validated_data.pop('language'))

        return user_profile
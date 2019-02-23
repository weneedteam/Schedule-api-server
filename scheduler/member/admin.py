from django.contrib import admin

from .models import User, UserProfile, FriendRequest


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('request_user', 'response_user', 'assent', )

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(FriendRequest, FriendRequestAdmin)
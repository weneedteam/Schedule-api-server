from django.contrib import admin

from .models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'registrant', 'start_time', 'state', )

admin.site.register(Schedule)
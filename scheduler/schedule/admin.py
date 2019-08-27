from django.contrib import admin

from .models import Schedule, Holiday


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'registrant', 'start_time', 'state', )


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_holiday', 'date', )
    list_filter = ('name', 'date', )


admin.site.register(Schedule)
admin.site.register(Holiday)

# attendance_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Group, Subject, Session, Attendance

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'profile__role')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else '-'
    get_role.short_description = 'Роль'

# Перерегистрируем User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'group')
    list_filter = ('group',)
    search_fields = ('title', 'group__name')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'teacher', 'start_time', 'end_time', 'created_at')
    list_filter = ('subject__group', 'teacher', 'start_time')
    search_fields = ('subject__title', 'teacher__username')
    date_hierarchy = 'start_time'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('session', 'student', 'timestamp')
    list_filter = ('session__subject__group', 'session__subject', 'student')
    search_fields = ('student__username', 'session__subject__title')
    date_hierarchy = 'timestamp'
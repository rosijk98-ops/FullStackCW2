from django.contrib import admin
from .models import (
    User, TrainerProfile, MemberProfile,
    WorkoutType, Location, FitnessClass,
    Schedule, Booking, WorkoutLog, Notification
)

# -------------------- Booking Inline --------------------
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 1

# -------------------- Booking Admin --------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('member', 'schedule', 'status', 'booked_at')
    search_fields = ('member__user__username', 'schedule__fitness_class__name')
    list_filter = ('status', 'schedule')
    ordering = ('-booked_at',)

# -------------------- MemberProfile Admin --------------------
@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')
    inlines = [BookingInline]

# -------------------- TrainerProfile Admin --------------------
@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

# -------------------- FitnessClass Admin --------------------
class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [ScheduleInline]

# -------------------- Schedule Admin --------------------
class BookingInlineForSchedule(admin.TabularInline):
    model = Booking
    extra = 1

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('fitness_class', 'start_time', 'end_time')
    inlines = [BookingInlineForSchedule]

# -------------------- Other Models --------------------
admin.site.register(User)
admin.site.register(WorkoutType)
admin.site.register(Location)

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'notes')
    search_fields = ('member__user__username', 'notes')
    list_filter = ('date',)
    ordering = ('-date',)

# -------------------- Notification Admin --------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_read', 'created_at')
    search_fields = ('title', 'user__username', 'message')
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)

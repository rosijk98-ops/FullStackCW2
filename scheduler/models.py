from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    MEMBER = 1
    TRAINER = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (MEMBER, 'Member'),
        (TRAINER, 'Trainer'),
        (ADMIN, 'Admin'),
    )
    
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=MEMBER)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    tfa_secret = models.CharField(max_length=255, blank=True) 

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': User.TRAINER})
    specialization = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Trainer: {self.user.get_full_name() or self.user.username}"

class MemberProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.MEMBER}
    )

    def __str__(self):
        return f"Member: {self.user.get_full_name() or self.user.username}"

class WorkoutType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100) 
    address = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=20)

    def __str__(self):
        return self.name

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    duration = models.DurationField()
    capacity = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)
    trainer = models.ForeignKey(
        'TrainerProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='classes'
    )

    def __str__(self):
        return f"{self.name} ({self.workout_type})"


class Schedule(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    start_time = models.DateTimeField() 
    end_time = models.DateTimeField()  

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trainer', 'start_time'], name='unique_trainer_time'),
            models.UniqueConstraint(fields=['location', 'start_time'], name='unique_location_time'),
        ]
        ordering = ['start_time']

    def save(self, *args, **kwargs):
        if not self.end_time and self.fitness_class:
            self.end_time = self.start_time + self.fitness_class.duration
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fitness_class.name} by {self.trainer} at {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    member = models.ForeignKey('MemberProfile', on_delete=models.CASCADE)  
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)  
    booked_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
        ('no_show', 'No-Show'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['member', 'schedule'], name='unique_member_booking'),
        ]
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.member.user.username} -> {self.schedule}"


class WorkoutLog(models.Model):
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.member} — {self.date}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
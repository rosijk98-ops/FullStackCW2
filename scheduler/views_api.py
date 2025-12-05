from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import MemberProfile, TrainerProfile, FitnessClass, Booking, Schedule
from .serializers import MemberSerializer, TrainerSerializer, FitnessClassSerializer, BookingSerializer, ScheduleSerializer


# MEMBER API

class MemberViewSet(viewsets.ModelViewSet):
    queryset = MemberProfile.objects.all()
    serializer_class = MemberSerializer


# TRAINER API

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerSerializer

# FITNESS CLASS API

class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'trainerprofile'):
            return FitnessClass.objects.filter(trainer=user.trainerprofile)
        return super().get_queryset()


# BOOKING API

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'trainerprofile'):
            return Booking.objects.filter(fitness_class__trainer=user.trainerprofile)
        return super().get_queryset()

# SCHEDULE API

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'trainerprofile'):
            return Schedule.objects.filter(trainer=user.trainerprofile)
        return super().get_queryset()

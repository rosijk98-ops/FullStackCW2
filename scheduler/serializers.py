from rest_framework import serializers
from .models import MemberProfile, TrainerProfile, FitnessClass, Booking, Schedule

class MemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MemberProfile
        fields = '__all__'

class TrainerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TrainerProfile
        fields = '__all__'

class FitnessClassSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source='trainer.user.username', read_only=True)

    class Meta:
        model = FitnessClass
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.user.username', read_only=True)
    fitness_class_name = serializers.CharField(source='fitness_class.name', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    fitness_class_name = serializers.CharField(source='fitness_class.name', read_only=True)
    trainer_name = serializers.CharField(source='trainer.user.username', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'

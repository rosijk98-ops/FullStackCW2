from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainerProfile, MemberProfile, FitnessClass, Location, Schedule, Booking, WorkoutLog
from django.contrib import messages
from .forms import (
    TrainerProfileForm, MemberProfileForm, FitnessClassForm,
    LocationForm, ScheduleForm, BookingForm, WorkoutLogForm
)
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from scheduler.models import Booking


# TRAINERPROFILE VIEWS
# CREATE
@login_required
def create_trainer(request):
    if request.method == "POST":
        form = TrainerProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trainer created successfully.")
            return redirect('trainers_list')
    else:
        form = TrainerProfileForm()
    return render(request, 'trainer/create_trainer.html', {'form': form})

# UPDATE
@login_required
@permission_required('scheduler.change_trainerprofile', raise_exception=True)
def update_trainer(request, pk):
    trainer = get_object_or_404(TrainerProfile, pk=pk)
    if request.method == "POST":
        form = TrainerProfileForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            messages.info(request, "Trainer updated successfully.")
            return redirect('trainers_list')
    else:
        form = TrainerProfileForm(instance=trainer)
    return render(request, 'trainer/update_trainer.html', {'form': form, 'trainer': trainer})

# DELETE
@login_required
@permission_required("fitness.delete_trainerprofile", raise_exception=True)
def delete_trainer(request, pk):
    trainer = get_object_or_404(TrainerProfile, pk=pk)
    if request.method == "POST":
        trainer.delete()
        messages.warning(request, "Trainer deleted.")
        return redirect('trainers_list')
    return render(request, 'trainer/delete_trainer.html', {'trainer': trainer})

# MEMBERPROFILE VIEWS

# CREATE
@login_required
def create_member(request):
    if request.method == "POST":
        form = MemberProfileForm(request.POST, user=request.user)  # передаем текущего пользователя
        if form.is_valid():
            form.save()
            messages.success(request, "Member created successfully.")
            return redirect('members_list')
    else:
        form = MemberProfileForm(user=request.user)
    return render(request, 'member/create_member.html', {'form': form})


# UPDATE
@login_required
def update_member(request, pk):
    member = get_object_or_404(MemberProfile, pk=pk)
    if request.user != member.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot edit this profile.")
    
    if request.method == "POST":
        form = MemberProfileForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.info(request, "Member updated successfully.")
            return redirect('members_list')
    else:
        form = MemberProfileForm(instance=member)
    return render(request, 'member/update_member.html', {'form': form, 'member': member})

# DELETE
@login_required
@permission_required("fitness.delete_memberprofile", raise_exception=True)
def delete_member(request, pk):
    member = get_object_or_404(MemberProfile, pk=pk)
    if request.method == "POST":
        member.delete()
        messages.warning(request, "Member deleted.")
        return redirect('members_list')
    return render(request, 'member/delete_member.html', {'member': member})

# FITNESSCLASS VIEWS
# CREATE
@login_required
def create_class(request):
    if request.method == "POST":
        form = FitnessClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class created successfully.")
            return redirect('fitness_class_list')
    else:
        form = FitnessClassForm()
    return render(request, 'class/create_class.html', {'form': form})

# UPDATE
@login_required
def update_class(request, pk):
    fitness_class = get_object_or_404(FitnessClass, pk=pk)
    if request.method == "POST":
        form = FitnessClassForm(request.POST, instance=fitness_class)
        if form.is_valid():
            form.save()
            messages.info(request, "Class updated successfully.")
            return redirect('fitness_class_list')
    else:
        form = FitnessClassForm(instance=fitness_class)
    return render(request, 'class/update_class.html', {'form': form, 'fitness_class': fitness_class})

# DELETE
@login_required
@permission_required("fitness.delete_fitnessclass", raise_exception=True)
def delete_class(request, pk):
    fitness_class = get_object_or_404(FitnessClass, pk=pk)
    if request.method == "POST":
        fitness_class.delete()
        messages.warning(request, "Class deleted.")
        return redirect('fitness_class_list')
    return render(request, 'class/delete_class.html', {'fitness_class': fitness_class})

# LOCATION VIEWS
@login_required
def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    schedules = Schedule.objects.filter(location=location).select_related('fitness_class', 'trainer', 'trainer__user')
    
    context = {
        'location': location,
        'schedules': schedules,
    }
    return render(request, 'location/location_detail.html', context)
# CREATE
@login_required
def create_location(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Location created successfully.")
            return redirect('locations_list')
    else:
        form = LocationForm()
    return render(request, 'location/create_location.html', {'form': form})

# UPDATE
@login_required
def update_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.info(request, "Location updated successfully.")
            return redirect('locations_list')
    else:
        form = LocationForm(instance=location)
    return render(request, 'location/update_location.html', {'form': form, 'location': location})

# DELETE
@login_required
@permission_required("fitness.delete_location", raise_exception=True)
def delete_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        location.delete()
        messages.warning(request, "Location deleted.")
        return redirect('locations_list')
    return render(request, 'location/delete_location.html', {'location': location})

# SCHEDULE VIEWS

# CREATE
@login_required
def create_schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule created successfully.")
            return redirect('schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'schedule/create_schedule.html', {'form': form})

# UPDATE
@login_required
def update_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.info(request, "Schedule updated successfully.")
            return redirect('schedule_list')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'schedule/update_schedule.html', {'form': form, 'schedule': schedule})

# DELETE
@login_required
@permission_required("fitness.delete_schedule", raise_exception=True)
def delete_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == "POST":
        schedule.delete()
        messages.warning(request, "Schedule deleted.")
        return redirect('schedule_list')
    return render(request, 'schedule/delete_schedule.html', {'schedule': schedule})



from django.shortcuts import render
from .models import User, TrainerProfile, MemberProfile, FitnessClass, Location, Schedule, Booking

@login_required
def home(request):
    user = request.user

    context = {
        'is_trainer': hasattr(user, "trainerprofile"),
        'is_member': hasattr(user, "memberprofile"),

        'trainer_count': TrainerProfile.objects.count(),
        'member_count': MemberProfile.objects.count(),
        'class_count': FitnessClass.objects.count(),
        'location_count': Location.objects.count(),
        'schedule_count': Schedule.objects.count(),
        'booking_count': Booking.objects.count(),
        'workoutlog_count': WorkoutLog.objects.count(),
    }
    return render(request, 'home.html', context)

# WORKOUTLOG VIEWS

# LIST
@login_required
def workoutlogs_list(request):
    logs = WorkoutLog.objects.select_related('member').all()
    return render(request, 'logs/workoutlogs_list.html', {'logs': logs})

# CREATE
@login_required
def create_workoutlog(request):
    if not hasattr(request.user, "memberprofile"):
        return HttpResponseForbidden("You are not allowed to create workout logs.")

    if request.method == "POST":
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            workoutlog = form.save(commit=False)
            workoutlog.member = MemberProfile.objects.get(user=request.user)
            workoutlog.save()
            messages.success(request, "Workout log created successfully.")
            return redirect('workoutlogs_list')
    else:
        form = WorkoutLogForm()
    return render(request, 'logs/create_workoutlog.html', {'form': form})

# UPDATE
@login_required
def update_workoutlog(request, pk):
    log = get_object_or_404(WorkoutLog, pk=pk)
    if request.method == "POST":
        form = WorkoutLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.info(request, "Workout log updated successfully.")
            return redirect('workoutlogs_list')
    else:
        form = WorkoutLogForm(instance=log)
    return render(request, 'logs/update_workoutlog.html', {'form': form, 'log': log})

# DELETE
@login_required
def delete_workoutlog(request, pk):
    log = get_object_or_404(WorkoutLog, pk=pk)
    if request.method == "POST":
        log.delete()
        messages.warning(request, "Workout log deleted.")
        return redirect('workoutlogs_list')
    return render(request, 'logs/delete_workoutlog.html', {'log': log})



@login_required
def trainers_list(request):
    trainers = TrainerProfile.objects.all()
    return render(request, 'trainer/trainers_list.html', {'trainers': trainers})

@login_required
def members_list(request):
    user = request.user

    if user.is_staff or hasattr(user, "trainerprofile"):
        members = MemberProfile.objects.all()
    elif hasattr(user, "memberprofile"):
        members = MemberProfile.objects.filter(user=user)
    else:
        members = MemberProfile.objects.none() 

    return render(request, 'member/members_list.html', {'members': members})

@login_required
def fitness_class_list(request):
    user = request.user

    if user.is_superuser:
        fitness_classes = FitnessClass.objects.all()
    elif hasattr(user, "trainerprofile"):
        fitness_classes = FitnessClass.objects.filter(trainer=user.trainerprofile)
    else:
        fitness_classes = FitnessClass.objects.all()

    return render(request, 'class/fitness_class_list.html', {'fitness_classes': fitness_classes})


@login_required
def locations_list(request):
    locations = Location.objects.all()
    return render(request, 'location/locations_list.html', {'locations': locations})
@login_required
def schedule_list(request):
    user = request.user

    if user.is_superuser:
        schedules = Schedule.objects.all()
    elif hasattr(user, "trainerprofile"):
        schedules = Schedule.objects.filter(fitness_class__trainer=user.trainerprofile)
    else:
        return HttpResponseForbidden("You are not allowed to view schedules.")

    return render(request, 'schedule/schedule_list.html', {'schedules': schedules})


@login_required
def bookings_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking/bookings_list.html', {'bookings': bookings})



@login_required
def workoutlogs_list(request):
    user = request.user

    if user.is_superuser:
        logs = WorkoutLog.objects.select_related("member").all()

    elif hasattr(user, "memberprofile"):
        logs = WorkoutLog.objects.filter(member__user=user)

    else:
        return HttpResponseForbidden("You are not allowed to view workout logs.")

    return render(request, 'logs/workoutlogs_list.html', {'logs': logs})

def custom_permission_denied_view(request, exception=None):
    return render(request, "403.html", status=403)


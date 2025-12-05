from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Booking, MemberProfile, Schedule
from .forms import BookingForm
from .models import WorkoutLog
from .forms import WorkoutLogForm
from django.http import HttpResponseForbidden
from .models import FitnessClass
from .forms import FitnessClassForm
from django.http import HttpResponseForbidden

## LIST 
class FitnessClassListView(LoginRequiredMixin, ListView):
    model = FitnessClass
    template_name = 'classes/class_list.html'
    context_object_name = 'classes'


# CREATE 
class FitnessClassCreateView(LoginRequiredMixin, CreateView):
    model = FitnessClass
    form_class = FitnessClassForm
    template_name = 'classes/class_form.html'
    success_url = reverse_lazy('classes_list')

    def dispatch(self, request, *args, **kwargs):
        is_trainer = hasattr(request.user, "trainerprofile")
        if not (request.user.is_superuser or is_trainer):
            return HttpResponseForbidden("Only staff can create classes.")
        return super().dispatch(request, *args, **kwargs)


# UPDATE 
class FitnessClassUpdateView(LoginRequiredMixin, UpdateView):
    model = FitnessClass
    form_class = FitnessClassForm
    template_name = 'classes/class_form.html'
    success_url = reverse_lazy('classes_list')

    def dispatch(self, request, *args, **kwargs):
        is_trainer = hasattr(request.user, "trainerprofile")
        if not (request.user.is_superuser or is_trainer):
            return HttpResponseForbidden("Only staff can edit classes.")
        return super().dispatch(request, *args, **kwargs)


# DELETE 
class FitnessClassDeleteView(LoginRequiredMixin, DeleteView):
    model = FitnessClass
    template_name = 'classes/class_confirm_delete.html'
    success_url = reverse_lazy('classes_list')

    def dispatch(self, request, *args, **kwargs):
        is_trainer = hasattr(request.user, "trainerprofile")
        if not (request.user.is_superuser or is_trainer):
            return HttpResponseForbidden("Only staff can delete classes.")
        return super().dispatch(request, *args, **kwargs)

class WorkoutLogListView(LoginRequiredMixin, ListView):
    model = WorkoutLog
    template_name = 'logs/log_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return WorkoutLog.objects.all()
        return WorkoutLog.objects.filter(member__user=user)


class WorkoutLogCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutLog
    form_class = WorkoutLogForm
    template_name = 'logs/log_form.html'
    success_url = reverse_lazy('logs_list')

    def form_valid(self, form):
        if not self.request.user.is_staff:
            form.instance.member = self.request.user.memberprofile
        return super().form_valid(form)


class WorkoutLogUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutLog
    form_class = WorkoutLogForm
    template_name = 'logs/log_form.html'
    success_url = reverse_lazy('logs_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_staff and obj.member.user != request.user:
            return HttpResponseForbidden("You cannot edit this log.")
        return super().dispatch(request, *args, **kwargs)


class WorkoutLogDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutLog
    template_name = 'logs/log_confirm_delete.html'
    success_url = reverse_lazy('logs_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_staff and obj.member.user != request.user:
            return HttpResponseForbidden("You cannot delete this log.")
        return super().dispatch(request, *args, **kwargs)


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/booking_list_cbv.html'
    context_object_name = 'bookings'
    ordering = ['-booked_at']

class BookingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form_cbv.html'
    success_url = reverse_lazy('bookings_list_cbv')
    permission_required = 'scheduler.add_booking'

    def form_valid(self, form):
        booking = form.save(commit=False)
        member = form.cleaned_data.get('member')
        schedule = form.cleaned_data.get('schedule')
        if member:
            booking.member = get_object_or_404(MemberProfile, id=member.id)
        if schedule:
            booking.schedule = get_object_or_404(Schedule, id=schedule.id)
        booking.save()
        messages.success(self.request, "Booking created successfully.")
        return super().form_valid(form)

class BookingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form_cbv.html'
    success_url = reverse_lazy('bookings_list_cbv')
    permission_required = 'scheduler.change_booking'

    def form_valid(self, form):
        messages.success(self.request, "Booking updated successfully.")
        return super().form_valid(form)

class BookingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking/booking_confirm_delete_cbv.html'
    success_url = reverse_lazy('bookings_list_cbv')
    permission_required = 'scheduler.delete_booking'

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "Booking deleted.")
        return super().delete(request, *args, **kwargs)


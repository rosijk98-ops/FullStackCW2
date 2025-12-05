from django.forms import ModelForm, DateInput, DateTimeInput
from django.forms.widgets import CheckboxInput, Select
from .models import TrainerProfile, MemberProfile, FitnessClass, Location, Schedule, Booking # Импортируем ваши модели
from django.core.exceptions import ValidationError
from django import forms
from .models import WorkoutLog


class DateInput(DateInput):
    """Виджет для поля даты с типом 'date'."""
    input_type = 'date'

class DateTimeLocalInput(DateTimeInput):
    """Виджет для поля даты и времени с типом 'datetime-local'."""
    input_type = 'datetime-local'


class BaseStyledModelForm(ModelForm):
    """Базовый класс для автоматического добавления CSS-класса 'form-control'."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, Select):
                widget.attrs['class'] = 'form-select'
            else:
                css = widget.attrs.get('class', '')
                widget.attrs['class'] = (css + ' form-control').strip()

class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                classes = f"{existing_classes} form-control".strip()
                field.widget.attrs['class'] = classes
        
        
class MemberProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=12)

    class Meta:
        model = MemberProfile
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone'].initial = getattr(self.instance.user, 'phone_number', '')

    def save(self, commit=True):
        member = super().save(commit=False)
        user = self.instance.user if self.instance.pk else self.user
        if user is None:
            raise ValueError("MemberProfile must be linked to a User.")

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone']

        if commit:
            user.save()
            member.user = user
            member.save()
        return member

class FitnessClassForm(forms.ModelForm):
    class Meta:
        model = FitnessClass
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

class LocationForm(BaseStyledModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class ScheduleForm(BaseStyledModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {
            'start_time': DateTimeLocalInput(),
            'end_time': DateTimeLocalInput(),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        member = cleaned_data.get('member')
        schedule = cleaned_data.get('schedule')

        if member and schedule:
            if Booking.objects.filter(member=member, schedule=schedule).exists():
                raise ValidationError("You are already registered for this class.")

            current_bookings = Booking.objects.filter(schedule__fitness_class=schedule.fitness_class).count()
            if current_bookings >= schedule.fitness_class.capacity:
                raise ValidationError("This class is fully booked. No more spots are available.")

        return cleaned_data

class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows':3})
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import TrainerProfile, MemberProfile, FitnessClass, Location, Schedule, Booking
import datetime

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Enter username'
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = 'Enter email'
            elif field_name in ['password1', 'password2']:
                field.widget.attrs['placeholder'] = 'Enter password'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
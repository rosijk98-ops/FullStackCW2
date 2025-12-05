from django.urls import path, include
from . import views
from .cbv import BookingListView, BookingCreateView, BookingUpdateView, BookingDeleteView

# --- DRF API ---
from rest_framework.routers import DefaultRouter
from .views_api import MemberViewSet, TrainerViewSet, FitnessClassViewSet, BookingViewSet, ScheduleViewSet

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'trainers', TrainerViewSet)
router.register(r'fitness-classes', FitnessClassViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'schedules', ScheduleViewSet)


urlpatterns = [
    # --- Web views ---
    path('', views.home, name='home'),
    path('trainers/', views.trainers_list, name='trainers_list'),
    path('members/', views.members_list, name='members_list'),
    path('locations/', views.locations_list, name='locations_list'),
    path('classes/', views.fitness_class_list, name='fitness_class_list'),
    path('schedule/', views.schedule_list, name='schedule_list'),

    # --- TrainerProfile CRUD ---
    path('trainers/add/', views.create_trainer, name='create_trainer'),
    path('trainers/<int:pk>/edit/', views.update_trainer, name='update_trainer'),
    path('trainers/<int:pk>/delete/', views.delete_trainer, name='delete_trainer'),

    # --- MemberProfile CRUD ---
    path('members/add/', views.create_member, name='create_member'),
    path('members/<int:pk>/edit/', views.update_member, name='update_member'),
    path('members/<int:pk>/delete/', views.delete_member, name='delete_member'),

    # --- FitnessClass CRUD ---
    path('classes/add/', views.create_class, name='create_class'),
    path('classes/<int:pk>/edit/', views.update_class, name='update_class'),
    path('classes/<int:pk>/delete/', views.delete_class, name='delete_class'),

    # --- Location CRUD ---
    path('locations/add/', views.create_location, name='create_location'),
    path('locations/<int:pk>/edit/', views.update_location, name='update_location'),
    path('locations/<int:pk>/delete/', views.delete_location, name='delete_location'),

    # --- Schedule CRUD ---
    path('schedule/add/', views.create_schedule, name='create_schedule'),
    path('schedule/<int:pk>/edit/', views.update_schedule, name='update_schedule'),
    path('schedule/<int:pk>/delete/', views.delete_schedule, name='delete_schedule'),

    # --- Workout Logs ---
    path('logs/', views.workoutlogs_list, name='workoutlogs_list'),
    path('logs/create/', views.create_workoutlog, name='create_workoutlog'),
    path('logs/<int:pk>/update/', views.update_workoutlog, name='update_workoutlog'),
    path('logs/<int:pk>/delete/', views.delete_workoutlog, name='delete_workoutlog'),

    # --- Booking CBV ---
    path('bookings/create/', BookingCreateView.as_view(), name='bookings_create_redirect'),
    path('bookings-cbv/', BookingListView.as_view(), name='bookings_list_cbv'),
    path('bookings-cbv/add/', BookingCreateView.as_view(), name='create_booking_cbv'),
    path('bookings-cbv/<int:pk>/edit/', BookingUpdateView.as_view(), name='update_booking_cbv'),
    path('bookings-cbv/<int:pk>/delete/', BookingDeleteView.as_view(), name='delete_booking_cbv'),

    # --- DRF API ---
    path('api/', include(router.urls)),
]

handler403 = "scheduling.views.custom_permission_denied_view"

# D:\rescue app\emergency_rescue_app\hospital\urls.py

from django.urls import path
from . import views  # Import all views from the hospital app

urlpatterns = [
    path('dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    # You might add other hospital-related URLs here later
]
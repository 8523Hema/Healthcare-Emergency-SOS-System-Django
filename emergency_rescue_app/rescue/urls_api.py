# # D:\rescue app\emergency_rescue_app\rescue\urls_api.py

# from django.urls import path
# from .views import SendEmergencyAlert, PatientDetailsAPIView

# urlpatterns = [
#     path('send_emergency/', SendEmergencyAlert.as_view(), name='send_emergency_alert'),
#     path('patient_details/<str:patient_id>/', PatientDetailsAPIView.as_view(), name='patient_details'),
# 

# D:\rescue app\emergency_rescue_app\rescue\urls_api.py

from django.urls import path
from .views import SendEmergencyAlert, PatientDetailsAPIView

urlpatterns = [
    path('send_emergency/', SendEmergencyAlert.as_view(), name='send_emergency_alert'),
    path('patient_details/<str:patient_id>/', PatientDetailsAPIView.as_view(), name='patient_details'),
]
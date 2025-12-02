

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from hospital.models import Patient
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from hospital.models import Patient, EmergencyAlert, Hospital
import json
import httpx
from asgiref.sync import sync_to_async

async def get_live_location(ip_address):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://ipapi.co/{ip_address}/json/')
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = response.json()
            return {
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude')
            }
    except httpx.RequestError as e:
        print(f"Error during request to ipapi.co: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error from ipapi.co: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        print(f"Error getting location: {e}")
        return None

# class SendEmergencyAlert(APIView):
#     async def post(self, request, *args, **kwargs):
#         patient_id = request.data.get('patient_id')
#         latitude = request.data.get('latitude')
#         longitude = request.data.get('longitude')

#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
        
#         location = await get_live_location(ip)
#         if location and location.get('latitude') and location.get('longitude'):
#             latitude = location['latitude']
#             longitude = location['longitude']

#         try:
#             patient = await sync_to_async(Patient.objects.get)(patient_id=patient_id)
#         except Patient.DoesNotExist:
#             return Response({'error': 'Invalid Patient ID'}, status=status.HTTP_404_NOT_FOUND)

#         if not all([latitude, longitude]):
#             return Response({'error': 'Latitude and Longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

#         emergency = await sync_to_async(EmergencyAlert.objects.create)(
#             patient=patient,
#             latitude=float(latitude),
#             longitude=float(longitude)
#         )

#         channel_layer = await sync_to_async(get_channel_layer)()
#         await channel_layer.group_send(
#             'emergency_alerts',
#             {
#                 'type': 'send_emergency_alert',
#                 'data': {
#                     'patient_name': patient.name,
#                     'patient_condition': patient.condition,
#                     'patient_id': patient.patient_id,
#                     'latitude': latitude,
#                     'longitude': longitude,
#                     'alert_id': emergency.id,
#                     'patient_details': {
#                         'allergies': patient.allergies,
#                         'blood_type': patient.blood_type,
#                         'medications': patient.medications,
#                         'emergency_contact': patient.emergency_contact,
#                         'health_summary': patient.health_summary
#                     }
#                 }
#             }
#         )

#         return Response({'success': 'Emergency alert sent successfully'}, status=status.HTTP_201_CREATED)
# class SendEmergencyAlert(APIView):
#     def post(self, request, *args, **kwargs):
#         patient_id = request.data.get('patient_id')
#         latitude = request.data.get('latitude')
#         longitude = request.data.get('longitude')

#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

#         location = async_to_sync(get_live_location)(ip)
#         if location and location.get('latitude') and location.get('longitude'):
#             latitude = location['latitude']
#             longitude = location['longitude']

#         try:
#             patient = Patient.objects.get(patient_id=patient_id)
#         except Patient.DoesNotExist:
#             return Response({'error': 'Invalid Patient ID'}, status=status.HTTP_404_NOT_FOUND)

#         if not all([latitude, longitude]):
#             return Response({'error': 'Latitude and Longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

#         emergency = EmergencyAlert.objects.create(
#             patient=patient,
#             latitude=float(latitude),
#             longitude=float(longitude)
#         )

#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'emergency_alerts',
#             {
#                 'type': 'send_emergency_alert',
#                 'data': {
#                     'patient_name': patient.name,
#                     'patient_condition': patient.condition,
#                     'patient_id': patient.patient_id,
#                     'latitude': latitude,
#                     'longitude': longitude,
#                     'alert_id': emergency.id,
#                     'patient_details': {
#                         'allergies': patient.allergies,
#                         'blood_type': patient.blood_type,
#                         'medications': patient.medications,
#                         'emergency_contact': patient.emergency_contact,
#                         'health_summary': patient.health_summary
#                     }
#                 }
#             }
#         )

#         return Response({'success': 'Emergency alert sent successfully'}, status=status.HTTP_201_CREATED)


class SendEmergencyAlert(APIView):
    def post(self, request, *args, **kwargs):
        patient_id = request.data.get('patient_id')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # ✅ Only fallback to IP if latitude or longitude missing
        if not latitude or not longitude:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            location = async_to_sync(get_live_location)(ip)

            if location and location.get('latitude') and location.get('longitude'):
                latitude = location['latitude']
                longitude = location['longitude']

        if not latitude or not longitude:
            return Response({'error': 'Latitude and Longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = Patient.objects.get(patient_id=patient_id)
        except Patient.DoesNotExist:
            return Response({'error': 'Invalid Patient ID'}, status=status.HTTP_404_NOT_FOUND)

        emergency = EmergencyAlert.objects.create(
            patient=patient,
            latitude=float(latitude),
            longitude=float(longitude)
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'emergency_alerts',
            {
                'type': 'send_emergency_alert',
                'data': {
                    'patient_name': patient.name,
                    'patient_condition': patient.condition,
                    'patient_id': patient.patient_id,
                    'latitude': latitude,
                    'longitude': longitude,
                    'alert_id': emergency.id,
                    'patient_details': {
                        'allergies': patient.allergies,
                        'blood_type': patient.blood_type,
                        'medications': patient.medications,
                        'emergency_contact': patient.emergency_contact,
                        'health_summary': patient.health_summary
                    }
                }
            }
        )

        return Response({'success': 'Emergency alert sent successfully'}, status=status.HTTP_201_CREATED)

class PatientDetailsAPIView(APIView):
    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(patient_id=patient_id)
            return Response({
                'name': patient.name,
                'allergies': patient.allergies,
                'blood_type': patient.blood_type,
                'condition': patient.condition,
                'medications': patient.medications,
                'emergency_contact': patient.emergency_contact,
                'health_summary': patient.health_summary
            })
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            patient = Patient.objects.get(username=username)
            if check_password(password, patient.password):
                request.session['patient_id'] = patient.patient_id
                return redirect('rescue_dashboard')
            else:
                return render(request, 'rescue/login.html', {'error': 'Invalid credentials'})
        except Patient.DoesNotExist:
            return render(request, 'rescue/login.html', {'error': 'Invalid credentials'})
    return render(request, 'rescue/login.html')

def rescue_dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')
    try:
        patient = Patient.objects.get(patient_id=patient_id)
        return render(request, 'rescue/dashboard.html', {'patient': patient})
    except Patient.DoesNotExist:
        return redirect('patient_login')

# This view seems to be from another part of your project,
# I'll include it to keep the file complete, but it is not
# directly modified for this request.
async def hospital_dashboard(request):
    alerts = await sync_to_async(EmergencyAlert.objects.filter)(is_resolved=False)
    alerts = await sync_to_async(alerts.order_by)('-timestamp')
    alerts_data = await sync_to_async(list)(alerts.values('id', 'latitude', 'longitude', 'timestamp', 'patient__name', 'patient__patient_id', 'patient__condition', 'patient__allergies', 'patient__blood_type', 'patient__medications', 'patient__emergency_contact', 'patient__health_summary'))
    
    hospitals = await sync_to_async(Hospital.objects.all)()
    print(f"Hospitals from DB in view: {hospitals}") # Debug print
    hospitals_data = [{'name': h.name, 'lat': h.latitude, 'lon': h.longitude} for h in hospitals]
    print(f"Hospitals data for JSON in view: {hospitals_data}") # Debug print
    
    context = {
        'alerts': alerts,
        'alerts_json': json.dumps(alerts_data), # Ensure alerts_data is also a JSON string
        'hospitals_json': json.dumps(hospitals_data or [])
# Ensure hospitals_data is always a JSON string
    }
    
    return render(request, 'hospital/dashboard.html', context)

def main_page(request):
    return render(request, 'rescue/main_page.html')

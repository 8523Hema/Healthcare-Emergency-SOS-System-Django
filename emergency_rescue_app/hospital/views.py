# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render
# from django.core.serializers import serialize
# from .models import EmergencyAlert
# import json

# def hospital_dashboard(request):
#     alerts_query = EmergencyAlert.objects.filter(is_resolved=False).order_by('-timestamp').select_related('patient')
    
#     # Serialize the alerts queryset into a list of dictionaries
#     alerts_data = []
#     for alert in alerts_query:
#         alerts_data.append({
#             'id': alert.id,
#             'latitude': alert.latitude,
#             'longitude': alert.longitude,
#             'patient_id': alert.patient.patient_id,
            
#             'patient_name': alert.patient.name,
#             'patient_condition': alert.patient.condition,
#             'timestamp': alert.timestamp.isoformat()
#         })

#     # Convert the list to a JSON string
#     alerts_json = json.dumps(alerts_data)
    
#     return render(request, 'hospital/dashboard.html', {'alerts_json': alerts_json})

from django.shortcuts import render
from hospital.models import EmergencyAlert, Hospital
import json

def hospital_dashboard(request):
    # --- Alerts Query ---
    alerts_query = EmergencyAlert.objects.filter(is_resolved=False).order_by('-timestamp').select_related('patient')
    alerts_data = []
    for alert in alerts_query:
        alerts_data.append({
            'id': alert.id,
            'latitude': alert.latitude,
            'longitude': alert.longitude,
            'patient_id': alert.patient.patient_id,
            'patient_name': alert.patient.name,
            'patient_condition': alert.patient.condition,
            'timestamp': alert.timestamp.isoformat()
        })

    alerts_json = json.dumps(alerts_data or [])  # always a JSON string

    # --- Hospitals Query ---
    hospitals_query = Hospital.objects.all()
    hospitals_data = []
    for h in hospitals_query:
        hospitals_data.append({
            'name': h.name,
            'lat': float(h.latitude),
            'lon': float(h.longitude)
        })

    hospitals_json = json.dumps(hospitals_data or [])  # always a JSON string

    # Debug prints
    print("✅ Final alerts_json:", alerts_json)
    print("✅ Final hospitals_json:", hospitals_json)

    return render(request, 'hospital/dashboard.html', {
        'alerts_json': alerts_json,
        'hospitals_json': hospitals_json
    })

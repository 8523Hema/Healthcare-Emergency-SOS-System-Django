
from django.urls import path
from .views import rescue_dashboard, patient_login
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', patient_login, name='patient_login'),
    path('dashboard/', rescue_dashboard, name='rescue_dashboard'),
    path('logout/', LogoutView.as_view(next_page='patient_login'), name='logout'),
]

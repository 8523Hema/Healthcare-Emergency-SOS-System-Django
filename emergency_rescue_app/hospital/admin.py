from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient, EmergencyAlert, Hospital
from django.contrib.auth.hashers import make_password
from django import forms

class PatientCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = '__all__'

class PatientAdmin(admin.ModelAdmin):
    form = PatientCreationForm
    list_display = ('name', 'patient_id', 'username', 'age', 'condition')
    search_fields = ('name', 'patient_id', 'username')

    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data:
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(Patient, PatientAdmin)
admin.site.register(EmergencyAlert)
admin.site.register(Hospital)

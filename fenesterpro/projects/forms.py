from django import forms
from .models import Project, WindowEntry

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client_name', 'client_address', 'client_phone', 'client_email', 'site_address', 'profile_system', 'status', 'notes']

class WindowEntryForm(forms.ModelForm):
    class Meta:
        model = WindowEntry
        fields = ['item_code', 'typology', 'width', 'height', 'quantity', 'glass_type', 'finish', 'has_mesh', 'location_note']

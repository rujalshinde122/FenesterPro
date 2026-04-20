from django import forms
from .models import Project, WindowEntry, Invoice

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client_name', 'client_address', 'client_phone', 'client_email', 'site_address', 'profile_system', 'status', 'notes']


class CustomerProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client_name', 'client_address', 'client_phone', 'client_email', 'site_address', 'profile_system', 'notes']

class WindowEntryForm(forms.ModelForm):
    class Meta:
        model = WindowEntry
        fields = ['item_code', 'typology', 'width', 'height', 'quantity', 'glass_type', 'finish', 'has_mesh', 'location_note']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['tax_percent', 'payment_status', 'notes']

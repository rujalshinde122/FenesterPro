"""Models for projects application."""
from django.db import models
from catalog.models import ProfileSystem, WindowTypology, GlassType, Finish, Profile

class Project(models.Model):
    project_code = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=255)
    client_address = models.TextField()
    client_phone = models.CharField(max_length=50)
    client_email = models.EmailField(blank=True)
    site_address = models.TextField(blank=True)
    profile_system = models.ForeignKey(ProfileSystem, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('draft', 'Draft'),
        ('quoted', 'Quoted'),
        ('confirmed', 'Confirmed'),
        ('in_production', 'In Production'),
        ('completed', 'Completed')
    ], default='draft')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.project_code} - {self.client_name}"

class WindowEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='windows')
    item_code = models.CharField(max_length=50, help_text="e.g. W01, D02")
    typology = models.ForeignKey(WindowTypology, on_delete=models.PROTECT)
    width = models.FloatField(help_text="in mm")
    height = models.FloatField(help_text="in mm")
    quantity = models.PositiveIntegerField(default=1)
    glass_type = models.ForeignKey(GlassType, on_delete=models.PROTECT)
    finish = models.ForeignKey(Finish, on_delete=models.PROTECT)
    has_mesh = models.BooleanField(default=False)
    location_note = models.CharField(max_length=255, blank=True)
    
    # Computed fields
    computed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_code} ({self.typology.code})"

class ComputedCutPiece(models.Model):
    window = models.ForeignKey(WindowEntry, on_delete=models.CASCADE, related_name='cut_pieces')
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    piece_name = models.CharField(max_length=255)
    length = models.FloatField(help_text="mm")
    quantity = models.IntegerField()
    total_length = models.FloatField(help_text="length * quantity * window.quantity")

    def __str__(self):
        return f"{self.window.item_code} - {self.piece_name} ({self.length}mm x {self.quantity})"

"""Models for optimizer application."""
from django.db import models
from projects.models import Project

class OptimisationResult(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='optimisation_result')
    created_at = models.DateTimeField(auto_now_add=True)
    total_bars_used = models.IntegerField(default=0)
    total_waste_mm = models.FloatField(default=0.0)
    overall_efficiency = models.FloatField(default=0.0)
    
    # The result will be stored as JSON
    result_data = models.JSONField(default=dict)

    def __str__(self):
        return f"Optimization for {self.project.project_code}"

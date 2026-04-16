"""Models for catalog application."""
from django.db import models

class ProfileSystem(models.Model):
    name = models.CharField(max_length=255)
    material = models.CharField(max_length=50, choices=[
        ('aluminium', 'Aluminium'),
        ('upvc', 'uPVC'),
        ('wood', 'Wood'),
        ('steel', 'Steel')
    ])
    standard_bar_length = models.FloatField(default=6000)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    system = models.ForeignKey(ProfileSystem, on_delete=models.CASCADE, related_name='profiles')
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=[
        ('frame', 'Frame'),
        ('sash', 'Sash'),
        ('mullion', 'Mullion'),
        ('transom', 'Transom'),
        ('bead', 'Bead'),
        ('other', 'Other')
    ])
    unit_weight = models.FloatField(help_text="kg/m")
    unit_cost = models.FloatField(help_text="INR per mm")

    def __str__(self):
        return f"{self.code} - {self.name}"

class GlassType(models.Model):
    name = models.CharField(max_length=255)
    thickness = models.FloatField(help_text="mm")
    cost_per_sqm = models.FloatField(help_text="INR")

    def __str__(self):
        return self.name

class Hardware(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=[
        ('handle', 'Handle'),
        ('hinge', 'Hinge'),
        ('lock', 'Lock'),
        ('roller', 'Roller'),
        ('seal', 'Seal'),
        ('other', 'Other')
    ])
    unit = models.CharField(max_length=50, choices=[
        ('per_unit', 'Per Unit'),
        ('per_metre', 'Per Metre'),
        ('per_window', 'Per Window')
    ])
    unit_cost = models.FloatField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Finish(models.Model):
    name = models.CharField(max_length=255)
    cost_factor = models.FloatField(default=1.0)

    def __str__(self):
        return self.name

class WindowTypology(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=[
        ('sliding', 'Sliding'),
        ('casement', 'Casement'),
        ('fixed', 'Fixed'),
        ('tilt_turn', 'Tilt & Turn'),
        ('awning', 'Awning'),
        ('door', 'Door')
    ])
    description = models.TextField()
    diagram_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class CuttingRule(models.Model):
    typology = models.ForeignKey(WindowTypology, on_delete=models.CASCADE, related_name='cutting_rules')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    piece_name = models.CharField(max_length=255)
    quantity_formula = models.CharField(max_length=255, help_text='e.g., "2" or "num_panels"')
    length_formula = models.CharField(max_length=255, help_text='e.g., "width - 2 * frame_deduction"')
    deduction_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.piece_name} for {self.typology.code}"

class CuttingRuleDeduction(models.Model):
    rule = models.ForeignKey(CuttingRule, on_delete=models.CASCADE, related_name='deductions')
    variable_name = models.CharField(max_length=100)
    value = models.FloatField(help_text="in mm")

    def __str__(self):
        return f"{self.variable_name} = {self.value}mm"

class HardwareRule(models.Model):
    typology = models.ForeignKey(WindowTypology, on_delete=models.CASCADE, related_name='hardware_rules')
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    quantity_formula = models.CharField(max_length=255, help_text='e.g., "2" or "num_panels * 2"')

    def __str__(self):
        return f"{self.hardware.name} for {self.typology.code}"

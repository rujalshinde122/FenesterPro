from django.core.management.base import BaseCommand
from catalog.models import (
    ProfileSystem, Profile, GlassType, Hardware, 
    Finish, WindowTypology, CuttingRule, CuttingRuleDeduction
)

class Command(BaseCommand):
    help = 'Seeds initial database data for FenesterPro demo.'

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # 1. Profile Systems
        ps, _ = ProfileSystem.objects.get_or_create(
            name="Aluminium 60mm Sliding Series",
            material="aluminium",
            standard_bar_length=6000,
            description="Premium aluminium sliding system."
        )

        # 2. Finishes
        mill, _ = Finish.objects.get_or_create(name="Mill Finish", cost_factor=1.0)
        pcw, _ = Finish.objects.get_or_create(name="Powder Coat White", cost_factor=1.2)

        # 3. Glass Types
        g5, _ = GlassType.objects.get_or_create(name="5mm Clear", thickness=5.0, cost_per_sqm=400)
        g6, _ = GlassType.objects.get_or_create(name="6mm Tinted", thickness=6.0, cost_per_sqm=550)

        # 4. Hardware
        h_handle, _ = Hardware.objects.get_or_create(name="Aluminium Handle", category="handle", unit="per_unit", unit_cost=250)
        h_roller, _ = Hardware.objects.get_or_create(name="Roller", category="roller", unit="per_unit", unit_cost=150)
        h_lock, _ = Hardware.objects.get_or_create(name="Security Lock", category="lock", unit="per_unit", unit_cost=300)

        # 5. Profiles
        profiles_data = [
            ("TF-01", "Top Frame", "frame", 0.9, 0.45),
            ("BF-01", "Bottom Frame", "frame", 1.1, 0.50),
            ("LF-01", "Left Frame", "frame", 0.9, 0.45),
            ("RF-01", "Right Frame", "frame", 0.9, 0.45),
            ("ST-01", "Sash Top", "sash", 0.7, 0.35),
            ("SB-01", "Sash Bottom", "sash", 0.8, 0.40),
            ("SL-01", "Sash Left", "sash", 0.7, 0.35),
            ("SR-01", "Sash Right", "sash", 0.7, 0.35),
            ("MT-01", "Middle Track", "mullion", 0.85, 0.42),
            ("BD-01", "Bead", "bead", 0.2, 0.10)
        ]
        
        profs = {}
        for code, name, role, weight, cost in profiles_data:
            p, _ = Profile.objects.get_or_create(
                system=ps, code=code,
                defaults={'name': name, 'role': role, 'unit_weight': weight, 'unit_cost': cost}
            )
            profs[code] = p

        # 6. Typologies
        sl2t, _ = WindowTypology.objects.get_or_create(
            code="SL2T", 
            defaults={
                'name': "Sliding 2-Track", 
                'category': "sliding", 
                'description': "Standard 2-track sliding window",
                'diagram_notes': "Standard offset."
            }
        )
        fx, _ = WindowTypology.objects.get_or_create(
            code="FX",
            defaults={
                'name': "Fixed Window",
                'category': "fixed",
                'description': "Standard fixed window",
            }
        )

        # 7. Cutting Rules for SL2T
        if sl2t.cutting_rules.count() == 0:
            rules_data = [
                (profs["TF-01"], "Top Frame", "1", "width"),
                (profs["BF-01"], "Bottom Frame", "1", "width"),
                (profs["LF-01"], "Left Frame", "1", "height - frame_deduction"),
                (profs["RF-01"], "Right Frame", "1", "height - frame_deduction"),
                (profs["ST-01"], "Sash Top", "num_panels", "(width / num_panels) + interlock_addition"),
                (profs["SB-01"], "Sash Bottom", "num_panels", "(width / num_panels) + interlock_addition"),
                (profs["SL-01"], "Sash Left", "num_panels", "height - sash_h_deduction"),
                (profs["SR-01"], "Sash Right", "num_panels", "height - sash_h_deduction"),
            ]
            for profile, p_name, qty_f, len_f in rules_data:
                cr = CuttingRule.objects.create(
                    typology=sl2t, profile=profile, piece_name=p_name,
                    quantity_formula=qty_f, length_formula=len_f
                )
                if "frame_deduction" in len_f:
                    CuttingRuleDeduction.objects.create(rule=cr, variable_name="frame_deduction", value=45.0)
                if "interlock_addition" in len_f:
                    CuttingRuleDeduction.objects.create(rule=cr, variable_name="interlock_addition", value=15.0)
                if "sash_h_deduction" in len_f:
                    CuttingRuleDeduction.objects.create(rule=cr, variable_name="sash_h_deduction", value=60.0)

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))

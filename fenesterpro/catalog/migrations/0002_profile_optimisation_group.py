from django.db import migrations, models


def populate_optimisation_groups(apps, schema_editor):
    Profile = apps.get_model('catalog', 'Profile')
    code_to_group = {
        'TF-01': 'FRAME-STD',
        'BF-01': 'FRAME-STD',
        'LF-01': 'FRAME-STD',
        'RF-01': 'FRAME-STD',
        'ST-01': 'SASH-STD',
        'SB-01': 'SASH-STD',
        'SL-01': 'SASH-STD',
        'SR-01': 'SASH-STD',
        'BD-01': 'BEAD-STD',
    }
    for code, group in code_to_group.items():
        Profile.objects.filter(code=code, optimisation_group='').update(optimisation_group=group)


def clear_optimisation_groups(apps, schema_editor):
    Profile = apps.get_model('catalog', 'Profile')
    Profile.objects.filter(
        optimisation_group__in=['FRAME-STD', 'SASH-STD', 'BEAD-STD']
    ).update(optimisation_group='')


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='optimisation_group',
            field=models.CharField(
                blank=True,
                help_text='Optional grouping key for interchangeable profiles during bar optimization.',
                max_length=100,
            ),
        ),
        migrations.RunPython(populate_optimisation_groups, clear_optimisation_groups),
    ]

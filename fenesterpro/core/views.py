from django.shortcuts import render
from projects.models import Project
from catalog.models import ProfileSystem

def dashboard(request):
    projects = Project.objects.all().order_by('-created_at')[:5]
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status__in=['draft', 'quoted', 'confirmed', 'in_production']).count()
    # Mock some data for the requirements
    windows_calculated = 150 # In a real app we might aggregate WindowEntry computed
    bars_saved = 45 # Same for optimisation efficiency
    
    context = {
        'recent_projects': projects,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'windows_calculated_month': windows_calculated,
        'bars_saved': bars_saved
    }
    return render(request, 'core/dashboard.html', context)

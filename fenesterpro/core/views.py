from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from projects.models import Project
from catalog.models import ProfileSystem
from projects.permissions import is_admin_user

def landing(request):
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(
        status__in=[Project.STATUS_PENDING, Project.STATUS_ACCEPTED, Project.STATUS_IN_PRODUCTION]
    ).count()
    profile_systems = ProfileSystem.objects.count()

    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'profile_systems': profile_systems,
    }
    return render(request, 'core/landing.html', context)

@login_required
def dashboard(request):
    admin_user = is_admin_user(request.user)
    qs = Project.objects.all() if admin_user else Project.objects.filter(customer=request.user)
    projects = qs.order_by('-created_at')[:5]
    total_projects = qs.count()
    active_projects = qs.filter(status__in=[Project.STATUS_PENDING, Project.STATUS_ACCEPTED, Project.STATUS_IN_PRODUCTION]).count()
    windows_calculated = sum(p.windows.filter(computed=True).count() for p in qs[:50])
    bars_saved = sum(1 for p in qs.select_related('optimisation_result') if hasattr(p, 'optimisation_result'))
    pending_approvals = Project.objects.filter(status=Project.STATUS_PENDING).count() if admin_user else 0
    
    context = {
        'recent_projects': projects,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'windows_calculated_month': windows_calculated,
        'bars_saved': bars_saved,
        'is_admin': admin_user,
        'pending_approvals': pending_approvals,
    }
    return render(request, 'core/dashboard.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('core:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Logged in successfully.")
            return redirect('core:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('core:landing')

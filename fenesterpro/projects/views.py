import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project, WindowEntry
from .forms import ProjectForm, WindowEntryForm
from calculator.engine import WindowCalculator
from optimizer.engine import BarOptimiser
from optimizer.models import OptimisationResult

def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            # Generate a simple unique project code
            project.project_code = f"PRJ-{str(uuid.uuid4())[:8].upper()}"
            project.save()
            messages.success(request, f"Project {project.project_code} created successfully.")
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    windows = project.windows.all()
    
    # Check if calculation and optimisation are done
    calculated_count = windows.filter(computed=True).count()
    all_calculated = windows.count() > 0 and calculated_count == windows.count()
    optimised = hasattr(project, 'optimisation_result')
    
    context = {
        'project': project,
        'windows': windows,
        'all_calculated': all_calculated,
        'optimised': optimised
    }
    return render(request, 'projects/project_detail.html', context)

def add_window(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = WindowEntryForm(request.POST)
        if form.is_valid():
            window = form.save(commit=False)
            window.project = project
            window.save()
            messages.success(request, "Window added successfully.")
            return redirect('projects:detail', pk=project.pk)
    else:
        # Default item code logic
        next_code = f"W{project.windows.count() + 1:02d}"
        form = WindowEntryForm(initial={'item_code': next_code})
    return render(request, 'projects/window_form.html', {'form': form, 'project': project})

def calculate_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        calculator = WindowCalculator()
        
        success_count = 0
        errors = []
        for window in project.windows.filter(computed=False):
            success, msg = calculator.calculate(window)
            if success:
                success_count += 1
            else:
                errors.append(f"{window.item_code}: {msg}")
                
        if errors:
            for error in errors:
                messages.error(request, error)
        if success_count > 0:
            messages.success(request, f"Successfully calculated {success_count} windows.")
            
    return redirect('projects:detail', pk=pk)

def optimise_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        
        # Gather all computed cut pieces
        cut_pieces = []
        for window in project.windows.filter(computed=True):
            for piece in window.cut_pieces.all():
                cut_pieces.append({
                    'profile_code': piece.profile.code,
                    'profile_name': piece.profile.name,
                    'piece_name': f"{window.item_code} - {piece.piece_name}",
                    'length': piece.length,
                    'qty': piece.quantity * window.quantity
                })
        
        if not cut_pieces:
            messages.warning(request, "No calculated cut pieces found for optimisation.")
            return redirect('projects:detail', pk=pk)
            
        optimiser = BarOptimiser(bar_length=project.profile_system.standard_bar_length if project.profile_system else 6000)
        result_data = optimiser.optimise(cut_pieces)
        
        # Save result
        OptimisationResult.objects.update_or_create(
            project=project,
            defaults={
                'total_bars_used': result_data.get('bars_used', 0),
                'total_waste_mm': result_data.get('waste_mm', 0.0),
                'overall_efficiency': 100.0 - result_data.get('waste_percent', 0.0), # Inverse
                'result_data': result_data
            }
        )
        messages.success(request, "Bar optimisation complete.")
    return redirect('projects:detail', pk=pk)

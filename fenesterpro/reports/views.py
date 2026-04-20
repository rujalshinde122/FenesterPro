import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from projects.models import Project
from projects.permissions import can_access_project
from .generators.quotation import generate_quotation_pdf
from .generators.boq import generate_boq_pdf
from .generators.cutting import generate_cutting_pdf
from .generators.excel import generate_excel


@login_required
def hub(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not can_access_project(request.user, project):
        return HttpResponse("Access denied.", status=403)
    return render(request, 'reports/hub.html', {'project': project})


@login_required
def quotation_report(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not can_access_project(request.user, project):
        return HttpResponse("Access denied.", status=403)
    result = generate_quotation_pdf(request, project)
    if isinstance(result, str):
        return HttpResponse(result)
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Quotation_{project.project_code}.pdf"'
    return response


@login_required
def boq_report(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not can_access_project(request.user, project):
        return HttpResponse("Access denied.", status=403)
    result = generate_boq_pdf(request, project)
    if isinstance(result, str):
        return HttpResponse(result)
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="BOQ_{project.project_code}.pdf"'
    return response


@login_required
def cutting_report(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not can_access_project(request.user, project):
        return HttpResponse("Access denied.", status=403)
    result = generate_cutting_pdf(request, project)
    if isinstance(result, str):
        return HttpResponse(result)
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="BarCutting_{project.project_code}.pdf"'
    return response


@login_required
def excel_report(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not can_access_project(request.user, project):
        return HttpResponse("Access denied.", status=403)
    workbook = generate_excel(project)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Project_{project.project_code}.xlsx"'
    workbook.save(response)
    return response

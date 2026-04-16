import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from projects.models import Project
from .generators.quotation import generate_quotation_pdf
from .generators.boq import generate_boq_pdf
from .generators.cutting import generate_cutting_pdf
from .generators.excel import generate_excel

def hub(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'reports/hub.html', {'project': project})

def quotation_report(request, pk):
    project = get_object_or_404(Project, pk=pk)
    result = generate_quotation_pdf(request, project)
    if isinstance(result, str):
        return HttpResponse(result)
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Quotation_{project.project_code}.pdf"'
    return response

def boq_report(request, pk):
    project = get_object_or_404(Project, pk=pk)
    result = generate_boq_pdf(request, project)
    if isinstance(result, str):
        return HttpResponse(result)
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="BOQ_{project.project_code}.pdf"'
    return response

def cutting_report(request, pk):
    project = get_object_or_404(Project, pk=pk)
    result = generate_cutting_pdf(request, project)
    if isinstance(result, str):
        return HttpResponse(result)
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="BarCutting_{project.project_code}.pdf"'
    return response

def excel_report(request, pk):
    project = get_object_or_404(Project, pk=pk)
    workbook = generate_excel(project)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Project_{project.project_code}.xlsx"'
    workbook.save(response)
    return response

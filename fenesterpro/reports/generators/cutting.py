from django.template.loader import render_to_string

def generate_cutting_pdf(request, project):
    opt_result = None
    if hasattr(project, 'optimisation_result'):
        opt_result = project.optimisation_result.result_data

    context = {
        'project': project,
        'opt_result': opt_result,
        'bar_length': project.profile_system.standard_bar_length if project.profile_system else 6000
    }

    html_string = render_to_string('reports/cutting_pdf.html', context)
    try:
        from weasyprint import HTML
        return HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    except OSError:
        # Fallback for Windows without GTK3
        return html_string


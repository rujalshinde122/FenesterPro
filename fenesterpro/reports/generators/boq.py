from django.template.loader import render_to_string

def generate_boq_pdf(request, project):
    # Gather cut pieces and aggregate
    pieces = {}
    for w in project.windows.filter(computed=True):
        for cp in w.cut_pieces.all():
            if cp.profile.code not in pieces:
                pieces[cp.profile.code] = {
                    'code': cp.profile.code,
                    'name': cp.profile.name,
                    'total_m': 0,
                    'cost': 0,
                    'items': []
                }
            
            p_len_m = cp.total_length / 1000
            pieces[cp.profile.code]['total_m'] += p_len_m
            pieces[cp.profile.code]['cost'] += (cp.total_length * cp.profile.unit_cost)
            pieces[cp.profile.code]['items'].append(cp)
            
    context = {
        'project': project,
        'profiles': pieces.values()
    }

    html_string = render_to_string('reports/boq_pdf.html', context)
    try:
        from weasyprint import HTML
        return HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    except OSError:
        # Fallback for Windows without GTK3
        return html_string

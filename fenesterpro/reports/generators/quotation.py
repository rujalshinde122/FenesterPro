from django.template.loader import render_to_string

# WeasyPrint requires GTK3, moving inside function to prevent Django startup crash on Windows

def generate_quotation_pdf(request, project):
    # Calculate totals for the quotation
    windows = project.windows.all()
    grand_total = 0
    items = []
    
    for w in windows:
        # Mock calculation of cost for demonstration
        # In reality, sum profiles, glass, hardware + finish multiplier
        unit_rate = (w.width * w.height / 1000000) * w.glass_type.cost_per_sqm * 2  # Very rough mock
        amount = unit_rate * w.quantity
        grand_total += amount
        
        items.append({
            'item_code': w.item_code,
            'location': w.location_note,
            'description': f"{w.typology.name} - {w.glass_type.name} ({w.finish.name})",
            'width': w.width,
            'height': w.height,
            'qty': w.quantity,
            'unit_rate': round(unit_rate, 2),
            'amount': round(amount, 2)
        })
        
    gst = grand_total * 0.18
    final_total = grand_total + gst

    context = {
        'project': project,
        'items': items,
        'subtotal': round(grand_total, 2),
        'gst': round(gst, 2),
        'total': round(final_total, 2),
    }

    html_string = render_to_string('reports/quotation_pdf.html', context)
    try:
        from weasyprint import HTML
        return HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    except OSError:
        # Fallback for Windows without GTK3
        return html_string

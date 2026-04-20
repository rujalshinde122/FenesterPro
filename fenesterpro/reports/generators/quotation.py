from django.template.loader import render_to_string

# WeasyPrint requires GTK3, moving inside function to prevent Django startup crash on Windows


def calculate_quotation_totals(project, tax_percent=18.0):
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
            'amount': round(amount, 2),
        })
    subtotal = round(grand_total, 2)
    tax_amount = round(subtotal * (tax_percent / 100), 2)
    total = round(subtotal + tax_amount, 2)
    return {
        'items': items,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total': total,
    }


def generate_quotation_pdf(request, project):
    pricing = calculate_quotation_totals(project, tax_percent=18.0)

    context = {
        'project': project,
        'items': pricing['items'],
        'subtotal': pricing['subtotal'],
        'gst': pricing['tax_amount'],
        'total': pricing['total'],
    }

    html_string = render_to_string('reports/quotation_pdf.html', context)
    try:
        from weasyprint import HTML
        return HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    except OSError:
        # Fallback for Windows without GTK3
        return html_string

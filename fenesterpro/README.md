# FenesterPro
**Window & Door Fabrication Management System**

FenesterPro is a complete production-ready web application built in Django, tailored for fabrication workshops to manage projects, calculate material cut lists, optimise bar usage (First-Fit Decreasing algorithm), and generate professional reports (PDF/Excel).

## Features
- **Project Tracking**: Manage window entries, dimensions, and typologies.
- **Dynamic Calculator Engine**: Parses and safely evaluates math string formulas configured dynamically in the catalog (e.g. `(width / 2) + 15`).
- **Bar Optimizer**: Computes efficiently packed material lengths and visualises wastage.
- **Reporting**: Quotation, Bill of Quantities, cutting layout PDFs (via WeasyPrint) and full data export to Excel (`openpyxl`).

## Installation

### Prerequisites
- Python 3.10+
- (Windows Only) GTK3 Runtime installed in your environment path or via MSYS2 if rendering PDFs locally using WeasyPrint.

```bash
# 1. Create simple Virtual Environment
python -m venv venv
# Activate on Windows
.\venv\Scripts\Activate.ps1
# Activate on Mac/Linux: source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup Env defaults
cp .env.example .env

# 4. Migrate database
python manage.py migrate

# 5. Populate required testing schemas & typologies
python manage.py seed_demo_data

# 6. Run Server
python manage.py runserver
```

## Creating new Typologies
To define new profiles (like an Awning window):
1. Create a `WindowTypology` via admin panel or Django shell.
2. Define `CuttingRules` mapped to `Profiles` providing exactly the parameter strings `width`, `height`, `num_panels`, and `num_tracks` in the evaluation strings.

## Deployment to DigitalOcean
1. Provision a basic Ubuntu Droplet and install python3.12-venv & nginx.
2. Transfer code, setup virtualenv, install requirements.
3. Configure Gunicorn to run as a systemd service pointing at `fenesterpro.wsgi:application`.
4. Configure Nginx as a reverse proxy passing requests to the internal Gunicorn socket, and serve staticfiles generated via `python manage.py collectstatic` on port 80.

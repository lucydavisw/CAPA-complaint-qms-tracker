# CAPA & Complaint Investigation Tracker App (QMS Prototype)

Simulates post-market QMS workflows:
- Complaints → Non-Conformances (NC) → CAPA/PFA
- KPI dashboard (closure times, overdue CAPAs, severity breakdown)
- CSV export for business/management reviews

**Standards:** ISO 13485, ISO 9001, FDA 21 CFR Part 820

## Quick Start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask db init
flask db migrate -m "init"
flask db upgrade
python seed.py
flask run


(You can add the SOP docs later the same way if you want.)

---

# 13) Initialize the database (Flask-Migrate) and run the app

**Initialize migration repo:**
```bash
flask db init

flask db migrate -m "init tables"

source .venv/bin/activate



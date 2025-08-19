from flask import render_template
from datetime import datetime
from .models import Complaint, CAPA, NonConformance
import statistics

def avg_days(start, end):
    if not start or not end:
        return None
    return (end - start).days

def register_kpi_routes(app):
    @app.route("/dashboard")
    def dashboard():
        complaints = Complaint.query.all()
        capas = CAPA.query.all()
        ncs = NonConformance.query.all()

        complaint_closures = [avg_days(c.reported_at, c.closed_at) for c in complaints if c.closed_at]
        capa_closures = [avg_days(c.created_at, c.closed_at) for c in capas if c.closed_at]

        kpis = {
            "complaints_total": len(complaints),
            "complaints_open": sum(1 for c in complaints if c.status != "Closed"),
            "capas_total": len(capas),
            "capas_open": sum(1 for c in capas if c.status != "Closed"),
            "ncs_total": len(ncs),
            "ncs_open": sum(1 for x in ncs if x.status != "Closed"),
            "avg_complaint_close_days": round(statistics.mean(complaint_closures),2) if complaint_closures else None,
            "avg_capa_close_days": round(statistics.mean(capa_closures),2) if capa_closures else None,
            "overdue_capa": sum(1 for c in capas if c.due_date and c.status != "Closed" and c.due_date < datetime.utcnow()),
        }
        by_severity = {}
        for c in complaints:
            by_severity[c.severity] = by_severity.get(c.severity, 0) + 1

        return render_template("dashboard.html", kpis=kpis, by_severity=by_severity)

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from . import db
from .models import User, Complaint, NonConformance, CAPA
from .forms import ComplaintForm, NCForm, CAPAForm
from datetime import datetime
import io, csv

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    open_complaints = Complaint.query.filter(Complaint.status != "Closed").count()
    open_capa = CAPA.query.filter(CAPA.status != "Closed").count()
    open_nc = NonConformance.query.filter(NonConformance.status != "Closed").count()
    return render_template("index.html", open_complaints=open_complaints, open_capa=open_capa, open_nc=open_nc)

@main_bp.route("/complaints")
def complaints():
    items = Complaint.query.order_by(Complaint.reported_at.desc()).all()
    return render_template("complaints.html", items=items)

@main_bp.route("/complaints/new", methods=["GET","POST"])
def complaints_new():
    form = ComplaintForm()
    if form.validate_on_submit():
        c = Complaint(
            title=form.title.data,
            description=form.description.data,
            customer=form.customer.data,
            severity=form.severity.data,
            category=form.category.data
        )
        db.session.add(c)
        db.session.commit()
        flash("Complaint created", "success")
        return redirect(url_for("main.complaints"))
    return render_template("complaints_new.html", form=form)

@main_bp.route("/complaints/<int:cid>")
def complaints_detail(cid):
    c = Complaint.query.get_or_404(cid)
    return render_template("complaints_detail.html", c=c)

@main_bp.route("/complaints/<int:cid>/close", methods=["POST"])
def complaints_close(cid):
    c = Complaint.query.get_or_404(cid)
    c.status = "Closed"
    c.closed_at = datetime.utcnow()
    db.session.commit()
    flash("Complaint closed", "success")
    return redirect(url_for("main.complaints_detail", cid=cid))

@main_bp.route("/complaints/export.csv")
def complaints_export():
    items = Complaint.query.order_by(Complaint.reported_at.desc()).all()
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["id","title","severity","category","status","reported_at","closed_at"])
    for x in items:
        writer.writerow([x.id,x.title,x.severity,x.category,x.status,x.reported_at,x.closed_at])
    mem = io.BytesIO()
    mem.write(out.getvalue().encode("utf-8"))
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name="complaints.csv", mimetype="text/csv")

@main_bp.route("/ncs")
def ncs():
    items = NonConformance.query.order_by(NonConformance.created_at.desc()).all()
    return render_template("ncs.html", items=items)

@main_bp.route("/ncs/new", methods=["GET","POST"])
def ncs_new():
    form = NCForm()
    if form.validate_on_submit():
        nc = NonConformance(
            source=form.source.data,
            process_area=form.process_area.data,
            description=form.description.data,
            complaint_id=form.complaint_id.data if form.complaint_id.data else None
        )
        db.session.add(nc)
        db.session.commit()
        flash("Non-Conformance created", "success")
        return redirect(url_for("main.ncs"))
    return render_template("ncs_new.html", form=form)

@main_bp.route("/ncs/<int:nc_id>/close", methods=["POST"])
def ncs_close(nc_id):
    nc = NonConformance.query.get_or_404(nc_id)
    nc.status = "Closed"
    nc.closed_at = datetime.utcnow()
    db.session.commit()
    flash("NC closed", "success")
    return redirect(url_for("main.ncs"))

@main_bp.route("/capas")
def capas():
    items = CAPA.query.order_by(CAPA.created_at.desc()).all()
    return render_template("capas.html", items=items)

@main_bp.route("/capas/new", methods=["GET","POST"])
def capas_new():
    form = CAPAForm()
    if form.validate_on_submit():
        due_dt = None
        if form.due_date.data:
            due_dt = datetime.strptime(form.due_date.data, "%Y-%m-%d")
        capa = CAPA(
            type=form.type.data,
            root_cause=form.root_cause.data,
            correction=form.correction.data,
            corrective_action=form.corrective_action.data,
            preventive_action=form.preventive_action.data,
            due_date=due_dt,
            nc_id=form.nc_id.data if form.nc_id.data else None,
            complaint_id=form.complaint_id.data if form.complaint_id.data else None
        )
        db.session.add(capa)
        db.session.commit()
        flash("CAPA created", "success")
        return redirect(url_for("main.capas"))
    return render_template("capas_new.html", form=form)

@main_bp.route("/capas/<int:cid>/status", methods=["POST"])
def capas_status(cid):
    capa = CAPA.query.get_or_404(cid)
    status = request.form.get("status")
    capa.status = status
    if status == "Closed":
        capa.closed_at = datetime.utcnow()
    db.session.commit()
    flash("CAPA status updated", "success")
    return redirect(url_for("main.capas"))

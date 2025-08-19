from datetime import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True)
    role = db.Column(db.String(50), default="quality")  # quality, support, r&d, product, legal

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))  # optional in seed; form uses it
    description = db.Column(db.Text, nullable=False)
    customer = db.Column(db.String(200))
    severity = db.Column(db.String(20))   # e.g., High/Medium/Low or Critical/Major/Minor
    category = db.Column(db.String(100))  # Product, Service, Installation, Cybersecurity, Other
    status = db.Column(db.String(20), default="Open")
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner = db.relationship("User", backref="complaints")

class NonConformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))  # complaint, audit, field, internal
    process_area = db.Column(db.String(120))  # e.g., Installation, Support, Dev, QMS
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Open")  # Open, Investigating, Corrected, Verified, Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner = db.relationship("User", backref="ncs")

    complaint_id = db.Column(db.Integer, db.ForeignKey("complaint.id"))
    complaint = db.relationship("Complaint", backref="ncs")

class CAPA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), default="Corrective")  # Corrective or Preventive (optional)
    description = db.Column(db.String(255), nullable=False)  # short summary of action/plan
    root_cause = db.Column(db.Text)              # optional
    correction = db.Column(db.Text)              # immediate fix
    corrective_action = db.Column(db.Text)       # addresses root cause
    preventive_action = db.Column(db.Text)       # prevents recurrence
    status = db.Column(db.String(20), default="Open")  # Open, Planned, Implemented, Verified, Closed
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner = db.relationship("User", backref="capas")

    nc_id = db.Column(db.Integer, db.ForeignKey("non_conformance.id"))
    nc = db.relationship("NonConformance", backref="capas")

    complaint_id = db.Column(db.Integer, db.ForeignKey("complaint.id"))
    complaint = db.relationship("Complaint", backref="capas")

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    action = db.Column(db.String(50))  # create, update, close
    who = db.Column(db.String(120))
    when = db.Column(db.DateTime, default=datetime.utcnow)
    before = db.Column(db.Text)
    after = db.Column(db.Text)

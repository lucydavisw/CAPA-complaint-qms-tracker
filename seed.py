from app import create_app, db
from app.models import User, Complaint, NonConformance, CAPA
from datetime import datetime, timedelta
import random

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    u_quality = User(name="Quality Owner", email="quality@example.com", role="quality")
    u_support = User(name="Support Lead", email="support@example.com", role="support")
    db.session.add_all([u_quality, u_support]); db.session.commit()

    # Complaints
    c1 = Complaint(
        title="Login error after software update",
        description="User cannot log in after v1.2.3; 500 returned by auth service.",
        customer="Customer A",
        severity="High",
        category="Product",
        status="Open"
    )
    c2 = Complaint(
        title="System freeze during data entry",
        description="UI becomes unresponsive after 10 minutes of continuous entry.",
        customer="Customer B",
        severity="Medium",
        category="Service",
        status="Closed",
        closed_at=datetime.utcnow() - timedelta(days=2)
    )
    db.session.add_all([c1, c2]); db.session.commit()

    # Non-Conformance linked to c1
    nc1 = NonConformance(
        source="complaint",
        process_area="Support",
        description="Patch did not resolve login error in prod; SOP step missing.",
        status="Open",
        complaint=c1,
        owner=u_quality
    )
    db.session.add(nc1); db.session.commit()

    # CAPA linked to nc1 and c1
    capa1 = CAPA(
        type="Corrective",
        description="Fix session handling; add validation test cases",
        root_cause="Improper session token validation in auth module",
        correction="Hotfix deployed to restore login",
        corrective_action="Update auth validation and unit tests",
        preventive_action="Add pre-release checklist and regression suite",
        status="Planned",
        due_date=datetime.utcnow() + timedelta(days=7),
        nc=nc1,
        complaint=c1,
        owner=u_quality
    )
    db.session.add(capa1); db.session.commit()

    print("✅ Database seeded with sample data!")

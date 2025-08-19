from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional

class ComplaintForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    customer = StringField("Customer", validators=[Optional()])
    severity = SelectField("Severity", choices=[("Critical","Critical"),("Major","Major"),("Minor","Minor")])
    category = SelectField("Category", choices=[("Product","Product"),("Service","Service"),("Installation","Installation"),("Cybersecurity","Cybersecurity"),("Other","Other")])
    submit = SubmitField("Create Complaint")

class NCForm(FlaskForm):
    source = SelectField("Source", choices=[("complaint","complaint"),("audit","audit"),("field","field"),("internal","internal")])
    process_area = StringField("Process Area", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    complaint_id = IntegerField("Complaint ID (optional)", validators=[Optional()])
    submit = SubmitField("Create NC")

class CAPAForm(FlaskForm):
    type = SelectField("Type", choices=[("Corrective","Corrective"),("Preventive","Preventive")])
    root_cause = TextAreaField("Root Cause", validators=[Optional()])
    correction = TextAreaField("Correction", validators=[Optional()])
    corrective_action = TextAreaField("Corrective Action", validators=[Optional()])
    preventive_action = TextAreaField("Preventive Action", validators=[Optional()])
    due_date = StringField("Due Date (YYYY-MM-DD)", validators=[Optional()])
    nc_id = IntegerField("Related NC ID", validators=[Optional()])
    complaint_id = IntegerField("Related Complaint ID", validators=[Optional()])
    submit = SubmitField("Create CAPA")

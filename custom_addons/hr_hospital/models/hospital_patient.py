from odoo import fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Пацієнт"
    _order = "name"

    name = fields.Char(required=True)
    birth_date = fields.Date()
    phone = fields.Char()
    email = fields.Char()
    attending_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        ondelete="set null",
    )
    disease_ids = fields.Many2many(
        comodel_name="hospital.disease",
        relation="hospital_patient_disease_rel",
        column1="patient_id",
        column2="disease_id",
        string="Diseases",
    )
    visit_ids = fields.One2many(
        comodel_name="hospital.patient.visit",
        inverse_name="patient_id",
        string="Visits",
    )
    notes = fields.Text()
    active = fields.Boolean(default=True)

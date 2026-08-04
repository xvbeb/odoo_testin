from odoo import fields, models


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Лікар"
    _order = "name"
    name = fields.Char(required=True)
    specialization = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    supervising_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        ondelete="set null",
    )
    patient_ids = fields.One2many(
        comodel_name="hospital.patient",
        inverse_name="attending_doctor_id",
        string="Patients",
    )
    visit_ids = fields.One2many(
        comodel_name="hospital.patient.visit",
        inverse_name="doctor_id",
        string="Visits",
    )
    active = fields.Boolean(default=True)

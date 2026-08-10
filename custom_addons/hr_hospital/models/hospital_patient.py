from odoo import fields, models


class HospitalPatient(models.Model):
    """ Взаїмовідносини пацієнта з лікарем та історія хвороб"""

    _name = "hospital.patient"
    _description = "Пацієнт"
    _inherit = "hospital.medic.info"
    _order = "name, id"

    name = fields.Char(string="ПІБ", required=True)
    phone = fields.Char(string="Телефон")
    email = fields.Char(string="Email")
    personal_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Персональний лікар",
        ondelete="set null",
    )
    doctor_history_ids = fields.One2many(
        comodel_name="hospital.doctor.history",
        inverse_name="patient_id",
        string="Історія персональних лікарів",
    )
    insurance_policy = fields.Char(
        string="Номер страхового поліса",
        size=20,
        copy=False,
    )
    disease_ids = fields.Many2many(
        comodel_name="hospital.disease",
        relation="hospital_patient_disease_rel",
        column1="patient_id",
        column2="disease_id",
        string="Хвороби",
    )
    visit_ids = fields.One2many(
        comodel_name="hospital.patient.visit",
        inverse_name="patient_id",
        string="Візити",
    )
    notes = fields.Text(string="Нотатки")
    active = fields.Boolean(default=True)

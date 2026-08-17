from odoo import api, fields, models


class HospitalPatient(models.Model):
    """ Взаїмовідносини пацієнта з лікарем та історія хвороб"""

    _name = "hospital.patient"
    _description = "Пацієнт"
    _inherit = "hospital.medic.info"
    _order = "name, id"

    name = fields.Char(string="ПІБ", required=True)
    phone = fields.Char(string="Телефон")
    email = fields.Char(string="Електронна пошта")
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
    active = fields.Boolean(string="Активний", default=True)
    visit_count = fields.Integer(string="Кількість візитів", compute="_compute_visit_count")

    @api.depends("visit_ids")
    def _compute_visit_count(self):
        for patient in self:
            patient.visit_count = len(patient.visit_ids)

    def action_open_visits(self):
        """Відкрити історію візитів поточного пацієнта."""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "hr_hospital.hospital_patient_visit_action"
        )
        action["domain"] = [("patient_id", "=", self.id)]
        action["context"] = {
            "default_patient_id": self.id,
            "default_doctor_id": self.personal_doctor_id.id,
        }
        return action

    def action_create_visit(self):
        """Створити та відкрити візит до персонального лікаря пацієнта."""
        self.ensure_one()
        visit = self.env["hospital.patient.visit"].create(
            {
                "patient_id": self.id,
                "doctor_id": self.personal_doctor_id.id,
                "scheduled_datetime": fields.Datetime.now(),
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Новий візит",
            "res_model": "hospital.patient.visit",
            "res_id": visit.id,
            "view_mode": "form",
            "target": "current",
        }

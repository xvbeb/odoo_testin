from odoo import fields, models


class HospitalPatientVisit(models.Model):
    _name = "hospital.patient.visit"
    _description = "Відвідування пацієнта"
    _order = "visit_datetime desc, id desc"
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        required=True,
        ondelete="cascade",
    )
    doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        required=True,
        ondelete="restrict",
    )
    visit_datetime = fields.Datetime(
        required=True,
        default=fields.Datetime.now,
    )
    disease_id = fields.Many2one(
        comodel_name="hospital.disease",
        ondelete="restrict",
    )
    diagnosis = fields.Text()
    recommendations = fields.Text()

    def _compute_display_name(self):
        for visit in self:
            visit.display_name = f"{visit.patient_id.name} — {visit.visit_datetime}"

from datetime import datetime, time

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VisitReportWizard(models.TransientModel):
    """ Звіт по візитах пацієнтів """

    _name = "visit.report.wizard"
    _description = "Звіт по візитах пацієнтів"

    doctor_ids = fields.Many2many(
        comodel_name="hospital.doctor",
        relation="visit_report_wizard_doctor_rel",
        string="Лікарі",
    )
    patient_ids = fields.Many2many(
        comodel_name="hospital.patient",
        relation="visit_report_wizard_patient_rel",
        string="Пацієнти",
    )
    date_from = fields.Date(string="Початок періоду")
    date_to = fields.Date(string="Кінець періоду")
    only_completed = fields.Boolean(string="Лише завершені візити")
    disease_id = fields.Many2one(
        comodel_name="hospital.disease",
        string="Хвороба",
        ondelete="set null",
    )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        active_model = self.env.context.get("active_model")
        active_ids = self.env.context.get("active_ids", [])
        if active_model == "hospital.doctor" and "doctor_ids" in fields_list:
            values["doctor_ids"] = [(6, 0, active_ids)]
        elif active_model == "hospital.patient" and "patient_ids" in fields_list:
            values["patient_ids"] = [(6, 0, active_ids)]
        return values

    @api.constrains("date_from", "date_to")
    def _check_period(self):
        for wizard in self:
            if wizard.date_from and wizard.date_to and wizard.date_to < wizard.date_from:
                raise ValidationError(
                    "Кінець періоду не може бути раніше початку періоду."
                )

    def action_show_visits(self):
        self.ensure_one()
        domain = []
        if self.doctor_ids:
            domain.append(("doctor_id", "in", self.doctor_ids.ids))
        if self.patient_ids:
            domain.append(("patient_id", "in", self.patient_ids.ids))
        if self.date_from:
            domain.append(
                (
                    "scheduled_datetime",
                    ">=",
                    fields.Datetime.to_string(datetime.combine(self.date_from, time.min)),
                )
            )
        if self.date_to:
            domain.append(
                (
                    "scheduled_datetime",
                    "<=",
                    fields.Datetime.to_string(datetime.combine(self.date_to, time.max)),
                )
            )
        if self.only_completed:
            domain.append(("state", "=", "done"))
        if self.disease_id:
            domain.append(("disease_id", "=", self.disease_id.id))

        return {
            "type": "ir.actions.act_window",
            "name": "Візити за критеріями звіту",
            "res_model": "hospital.patient.visit",
            "view_mode": "list,calendar,form",
            "domain": domain,
            "context": {"create": False},
        }

from datetime import datetime, time

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DiseaseMonthReportWizard(models.TransientModel):
    _name = "disease.month.report.wizard"
    _description = "Звіт по захворюваннях за період"

    doctor_ids = fields.Many2many(
        comodel_name="hospital.doctor",
        relation="disease_month_report_doctor_rel",
        string="Лікарі",
    )
    disease_ids = fields.Many2many(
        comodel_name="hospital.disease",
        relation="disease_month_report_disease_rel",
        string="Захворювання",
    )
    date_from = fields.Date(
        string="З",
        required=True,
        default=lambda self: fields.Date.start_of(
            fields.Date.context_today(self), "month"
        ),
    )
    date_to = fields.Date(
        string="По",
        required=True,
        default=lambda self: fields.Date.end_of(
            fields.Date.context_today(self), "month"
        ),
    )

    @api.constrains("date_from", "date_to")
    def _check_period(self):
        for wizard in self:
            if wizard.date_to < wizard.date_from:
                raise ValidationError("Дата «По» не може бути раніше дати «З».")

    def action_show_report(self):
        self.ensure_one()
        domain = [
            (
                "scheduled_datetime",
                ">=",
                fields.Datetime.to_string(datetime.combine(self.date_from, time.min)),
            ),
            (
                "scheduled_datetime",
                "<=",
                fields.Datetime.to_string(datetime.combine(self.date_to, time.max)),
            ),
        ]
        if self.doctor_ids:
            domain.append(("doctor_id", "in", self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(("disease_id", "in", self.disease_ids.ids))

        action = self.env["ir.actions.actions"]._for_xml_id(
            "hr_hospital.hospital_patient_visit_action"
        )
        action.update(
            {
                "name": "Звіт по захворюваннях",
                "view_mode": "list,form",
                "views": [
                    (
                        self.env.ref(
                            "hr_hospital.hospital_patient_visit_view_list"
                        ).id,
                        "list",
                    ),
                    (False, "form"),
                ],
                "domain": domain,
                "context": {"group_by": "disease_id", "create": False},
            }
        )
        return action

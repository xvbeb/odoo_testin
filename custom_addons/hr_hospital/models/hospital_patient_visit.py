from odoo import api, fields, models
from odoo.exceptions import UserError


class HospitalPatientVisit(models.Model):
    """Візити за розкладом та фактичні візити пацієнтів."""

    _name = "hospital.patient.visit"
    _description = "Візит пацієнта"
    _order = "scheduled_datetime desc, id desc"

    state = fields.Selection(
        selection=[
            ("planned", "Заплановано"),
            ("done", "Завершено"),
            ("cancelled", "Скасовано"),
        ],
        string="Статус",
        required=True,
        default="planned",
        index=True,
    )
    scheduled_datetime = fields.Datetime(
        string="Запланована дата та час",
        required=True,
        default=fields.Datetime.now,
        index=True,
    )
    actual_datetime = fields.Datetime(string="Фактична дата та час")
    doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Лікар",
        required=True,
        ondelete="restrict",
        index=True,
    )
    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="Пацієнт",
        required=True,
        ondelete="cascade",
        index=True,
    )
    summary = fields.Html(string="Епікриз")
    disease_id = fields.Many2one(
        comodel_name="hospital.disease",
        string="Хвороба",
        ondelete="restrict",
    )
    active = fields.Boolean(string="Активний", default=True)
    disease_visit_count = fields.Integer(
        string="Кількість візитів із цією хворобою",
        compute="_compute_disease_visit_count",
    )

    @api.depends("disease_id")
    def _compute_disease_visit_count(self):
        for visit in self:
            visit.disease_visit_count = (
                self.search_count([("disease_id", "=", visit.disease_id.id)])
                if visit.disease_id
                else 0
            )

    def action_open_disease_visits(self):
        """Відкрити всі візити, пов'язані з поточним захворюванням."""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "hr_hospital.hospital_patient_visit_action"
        )
        action["domain"] = [("disease_id", "=", self.disease_id.id)]
        action["context"] = {"default_disease_id": self.disease_id.id}
        return action

    @api.depends("patient_id.name", "doctor_id.name", "scheduled_datetime")
    def _compute_display_name(self):
        for visit in self:
            visit.display_name = (
                f"{visit.patient_id.name or ''} - {visit.doctor_id.name or ''} "
                f"({visit.scheduled_datetime or ''})"
            )

    def write(self, vals):
        protected_fields = {"scheduled_datetime", "actual_datetime", "doctor_id", "state"}
        for visit in self:
            if visit.state == "done" and (
                protected_fields.intersection(vals)
                or vals.get("active") is False
            ):
                raise UserError(
                    "Не можна змінювати дату, час, лікаря, статус або "
                    "архівувати завершений візит."
                )
        return super().write(vals)

    def unlink(self):
        is_hospital_admin = self.env.user.has_group(
            "hr_hospital.group_hospital_administrator"
        )
        if not is_hospital_admin and any(visit.state == "done" for visit in self):
            raise UserError("Не можна видаляти завершені візити.")
        return super().unlink()

from odoo import api, fields, models
from odoo.exceptions import UserError


class HospitalPatientVisit(models.Model):
    """ Візити за роскладом та фактичні візити пацієнтів """

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
    summary = fields.Html(string="Епікриз / Summary")
    disease_id = fields.Many2one(
        comodel_name="hospital.disease",
        string="Хвороба",
        ondelete="restrict",
    )
    active = fields.Boolean(default=True)

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
        if any(visit.state == "done" for visit in self):
            raise UserError("Не можна видаляти завершені візити.")
        return super().unlink()

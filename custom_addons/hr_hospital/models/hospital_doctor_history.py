from odoo import api, fields, models


class HospitalDoctorHistory(models.Model):
    """Зберігати історію призначення персональних лікарів пацієнтам."""

    _name = "hospital.doctor.history"
    _description = "Історія персональних лікарів"
    _order = "assignment_date desc, id desc"

    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="Пацієнт",
        required=True,
        ondelete="cascade",
    )
    doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Лікар",
        required=True,
        ondelete="restrict",
    )
    assignment_date = fields.Date(
        string="Дата призначення",
        required=True,
        default=fields.Date.context_today,
    )
    change_date = fields.Date(string="Дата зміни лікаря")
    active = fields.Boolean(string="Активний", default=True)

    @api.onchange("assignment_date", "change_date")
    def _onchange_dates(self):
        """Попередити користувача про некоректну послідовність дат."""
        if (
            self.assignment_date
            and self.change_date
            and self.change_date < self.assignment_date
        ):
            return {
                "warning": {
                    "title": "Некоректна дата",
                    "message": (
                        "Дата зміни лікаря не може бути раніше ніж дата "
                        "призначення"
                    ),
                }
            }
        return None

    @api.depends(
        "patient_id.name",
        "doctor_id.name",
        "doctor_id.category_id.name",
        "assignment_date",
    )
    def _compute_display_name(self):
        """Сформувати назву запису історії з пацієнта, лікаря та дати."""
        for history in self:
            patient = history.patient_id.name or ""
            doctor = history.doctor_id.name or ""
            category = history.doctor_id.category_id.name or "Без категорії"
            assignment_date = history.assignment_date or ""
            history.display_name = (
                f"{patient} - {doctor} ({category}) {assignment_date}"
            )

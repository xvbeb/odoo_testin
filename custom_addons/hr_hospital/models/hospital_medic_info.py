from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class HospitalMedicInfo(models.AbstractModel):
    """Надавати спільні медичні поля для лікарів і пацієнтів."""

    _name = "hospital.medic.info"
    _description = "Медична інформація"

    blood_group = fields.Selection(
        selection=[
            ("o_positive", "O(I) Rh+"),
            ("o_negative", "O(I) Rh-"),
            ("a_positive", "A(II) Rh+"),
            ("a_negative", "A(II) Rh-"),
            ("b_positive", "B(III) Rh+"),
            ("b_negative", "B(III) Rh-"),
            ("ab_positive", "AB(IV) Rh+"),
            ("ab_negative", "AB(IV) Rh-"),
        ],
        string="Група крові",
    )
    gender = fields.Selection(
        selection=[("male", "Чоловік"), ("female", "Жінка")],
        string="Стать",
    )
    birth_date = fields.Date(string="Дата народження")
    age = fields.Integer(string="Вік", compute="_compute_age")

    @api.depends("birth_date")
    def _compute_age(self):
        """Обчислити повний вік запису за датою народження."""
        for record in self:
            today = fields.Date.context_today(record)
            record.age = (
                relativedelta(today, record.birth_date).years
                if record.birth_date
                else 0
            )

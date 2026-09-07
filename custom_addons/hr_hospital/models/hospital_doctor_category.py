from odoo import fields, models


class HospitalDoctorCategory(models.Model):
    """Зберігати категорії кваліфікації лікарів."""

    _name = "hospital.doctor.category"
    _description = "Кваліфікація лікаря"
    _order = "sequence, name, id"

    name = fields.Char(string="Назва", required=True)
    sequence = fields.Integer(string="Послідовність", default=10)
    doctor_ids = fields.One2many(
        comodel_name="hospital.doctor",
        inverse_name="category_id",
        string="Лікарі",
    )
    is_intern = fields.Boolean(
        string="Категорія інтернів",
        default=False,
    )

    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "Кваліфікація лікаря з такою назвою вже існує.",
    )

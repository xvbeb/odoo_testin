from odoo import fields, models


class HospitalDisease(models.Model):
    _name = "hospital.disease"
    _description = "Хвороба"
    _order = "name"
    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "The disease name must be unique.",
    )

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDisease(models.Model):
    """ Ієрархія хвороб """

    _name = "hospital.disease"
    _description = "Хвороба"
    _order = "name, id"
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(string="Назва", required=True, translate=True)
    description = fields.Text(string="Опис", translate=True)
    parent_id = fields.Many2one(
        comodel_name="hospital.disease",
        string="Батьківська хвороба",
        index=True,
        ondelete="restrict",
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many(
        comodel_name="hospital.disease",
        inverse_name="parent_id",
        string="Дочірні хвороби",
    )
    display_name = fields.Char(compute="_compute_display_name", recursive=True)
    active = fields.Boolean(string="Активний", default=True)

    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "Хвороба з такою назвою вже існує.",
    )

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        if self._has_cycle():
            raise ValidationError("Ієрархія хвороб не може містити цикли.")

    @api.depends("name", "parent_id.display_name")
    def _compute_display_name(self):
        for disease in self:
            names = []
            current = disease
            while current:
                names.append(current.name or "")
                current = current.parent_id
            disease.display_name = " / ".join(reversed(names))

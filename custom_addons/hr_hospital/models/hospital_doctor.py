from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    """ Лікарі та їхня інформація """

    _name = "hospital.doctor"
    _description = "Лікар"
    _inherit = "hospital.medic.info"
    _order = "name, id"

    name = fields.Char(string="ПІБ", required=True)
    specialization = fields.Char(string="Спеціалізація")
    phone = fields.Char(string="Телефон")
    email = fields.Char(string="Електронна пошта")
    category_id = fields.Many2one(
        comodel_name="hospital.doctor.category",
        string="Категорія",
        ondelete="restrict",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Користувач системи",
        ondelete="set null",
    )
    is_intern = fields.Boolean(
        string="Лікар є інтерном",
        compute="_compute_is_intern",
        store=True,
    )
    mentor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Ментор",
        ondelete="set null",
    )
    intern_ids = fields.One2many(
        comodel_name="hospital.doctor",
        inverse_name="mentor_id",
        string="Інтерни",
    )
    mentor_specialization = fields.Char(
        string="Спеціалізація ментора",
        related="mentor_id.specialization",
    )
    mentor_category_id = fields.Many2one(
        comodel_name="hospital.doctor.category",
        string="Категорія ментора",
        related="mentor_id.category_id",
    )
    mentor_phone = fields.Char(string="Телефон ментора", related="mentor_id.phone")
    mentor_email = fields.Char(
        string="Електронна пошта ментора",
        related="mentor_id.email",
    )
    patient_ids = fields.One2many(
        comodel_name="hospital.patient",
        inverse_name="personal_doctor_id",
        string="Пацієнти",
    )
    visit_ids = fields.One2many(
        comodel_name="hospital.patient.visit",
        inverse_name="doctor_id",
        string="Візити",
    )
    active = fields.Boolean(string="Активний", default=True)

    @api.depends("category_id")
    def _compute_is_intern(self):
        intern_category = self.env.ref(
            "hr_hospital.doctor_category_intern",
            raise_if_not_found=False,
        )
        for doctor in self:
            doctor.is_intern = bool(
                intern_category and doctor.category_id == intern_category
            )

    @api.constrains("mentor_id")
    def _check_mentor_is_not_intern(self):
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError("Лікар-інтерн не може бути ментором.")

    @api.constrains("mentor_id")
    def _check_mentor_is_not_self(self):
        for doctor in self:
            if doctor.mentor_id == doctor:
                raise ValidationError("Лікар не може бути власним ментором.")

    def action_schedule_visit(self):
        """Відкрити форму нового візиту з попередньо обраним лікарем."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Швидкий запис до лікаря",
            "res_model": "hospital.patient.visit",
            "view_mode": "form",
            "target": "current",
            "context": {"default_doctor_id": self.id},
        }

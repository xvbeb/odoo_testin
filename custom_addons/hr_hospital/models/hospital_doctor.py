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
    email = fields.Char(string="Email")
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
    active = fields.Boolean(default=True)

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

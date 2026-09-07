from odoo import fields, models
from odoo.exceptions import UserError


class MassReassignDoctorWizard(models.TransientModel):
    """Масово змінювати персонального лікаря для обраних пацієнтів."""

    _name = "mass.reassign.doctor.wizard"
    _description = "Масове перевизначення персонального лікаря"

    new_doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Новий лікар",
        required=True,
        domain=[("is_intern", "=", False)],
    )
    change_date = fields.Date(
        string="Дата зміни",
        required=True,
        default=fields.Date.context_today,
    )

    def action_reassign(self):
        """Перепризначити лікаря та оновити історію вибраних пацієнтів."""
        self.ensure_one()
        if self.env.context.get("active_model") != "hospital.patient":
            raise UserError("Візард потрібно викликати зі списку пацієнтів.")

        patients = self.env["hospital.patient"].browse(
            self.env.context.get("active_ids", [])
        ).exists()
        if not patients:
            raise UserError("Оберіть хоча б одного пацієнта.")

        History = self.env["hospital.doctor.history"]
        active_history = History.search(
            [("patient_id", "in", patients.ids), ("active", "=", True)]
        )
        active_history.write(
            {"change_date": self.change_date, "active": False}
        )

        patients.write({"personal_doctor_id": self.new_doctor_id.id})
        History.create(
            [
                {
                    "patient_id": patient.id,
                    "doctor_id": self.new_doctor_id.id,
                    "assignment_date": self.change_date,
                    "active": True,
                }
                for patient in patients
            ]
        )
        return {"type": "ir.actions.act_window_close"}

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestHospitalModels(TransactionCase):
    """Перевіряти основну бізнес-логіку моделей лікарні."""

    @classmethod
    def setUpClass(cls):
        """Створити спільні категорії, лікаря та пацієнта для тестів."""
        super().setUpClass()
        cls.intern_category = cls.env.ref(
            "hr_hospital.doctor_category_intern"
        )
        cls.specialist_category = cls.env.ref(
            "hr_hospital.doctor_category_specialist"
        )
        cls.doctor = cls.env["hospital.doctor"].create(
            {
                "name": "Test Doctor",
                "specialization": "Therapy",
                "category_id": cls.specialist_category.id,
            }
        )
        cls.patient = cls.env["hospital.patient"].create(
            {
                "name": "Test Patient",
                "birth_date": "2000-01-15",
                "personal_doctor_id": cls.doctor.id,
            }
        )

    def test_patient_age_is_computed_from_birth_date(self):
        """The shared medical model computes age from the birth date."""
        expected_age = relativedelta(
            fields.Date.context_today(self.patient),
            self.patient.birth_date,
        ).years

        self.assertEqual(self.patient.age, expected_age)

    def test_intern_cannot_be_assigned_as_mentor(self):
        """An intern must never mentor another doctor."""
        intern = self.env["hospital.doctor"].create(
            {
                "name": "Test Intern",
                "category_id": self.intern_category.id,
                "mentor_id": self.doctor.id,
            }
        )

        with self.assertRaises(ValidationError):
            self.env["hospital.doctor"].create(
                {
                    "name": "Second Test Intern",
                    "category_id": self.intern_category.id,
                    "mentor_id": intern.id,
                }
            )

    def test_schedule_visit_action_sets_current_doctor(self):
        """The kanban action opens a visit form with a default doctor."""
        action = self.doctor.action_schedule_visit()

        self.assertEqual(action["res_model"], "hospital.patient.visit")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["context"]["default_doctor_id"], self.doctor.id)

    def test_completed_visit_protects_important_fields(self):
        """A completed visit cannot have its schedule changed or be archived."""
        visit = self.env["hospital.patient.visit"].create(
            {
                "doctor_id": self.doctor.id,
                "patient_id": self.patient.id,
                "state": "done",
            }
        )

        with self.assertRaises(UserError):
            visit.write({"scheduled_datetime": fields.Datetime.now()})

        with self.assertRaises(UserError):
            visit.write({"active": False})

        self.assertTrue(visit.write({"summary": "Updated conclusion"}))

# Порядок імпорту важливий: абстрактна модель завантажується першою.
# ruff: noqa: I001

from . import (
    hospital_medic_info,
    hospital_disease,
    hospital_doctor_category,
    hospital_doctor,
    hospital_doctor_history,
    hospital_patient,
    hospital_patient_visit,
)

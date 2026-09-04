from odoo import SUPERUSER_ID, api


DISEASE_VALUES = {
    "hospital_disease_influenza": {
        "name": "Influenza",
        "description": "Acute viral respiratory infection.",
    },
    "hospital_disease_hypertension": {
        "name": "Hypertension",
        "description": "Persistent elevation of arterial blood pressure.",
    },
    "hospital_disease_diabetes": {
        "name": "Diabetes mellitus",
        "description": "Disorder of blood glucose regulation.",
    },
}


def migrate(cr, version):
    """Set English source values before loading Ukrainian translations."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    for xmlid, values in DISEASE_VALUES.items():
        disease = env.ref(f"hr_hospital.{xmlid}", raise_if_not_found=False)
        if disease:
            disease.with_context(lang="en_US").write(values)

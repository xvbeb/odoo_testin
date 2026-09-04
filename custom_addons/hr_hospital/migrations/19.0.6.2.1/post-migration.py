from odoo import SUPERUSER_ID, api


DISEASE_VALUES = {
    "hospital_disease_respiratory": {
        "name": "Respiratory system diseases",
        "description": "Demonstration parent category.",
    },
    "hospital_disease_viral_respiratory": {
        "name": "Viral respiratory infections",
    },
    "hospital_disease_covid": {
        "name": "COVID-19",
    },
    "hospital_disease_cardiovascular": {
        "name": "Cardiovascular diseases",
    },
    "hospital_disease_arrhythmia": {
        "name": "Arrhythmia",
    },
}


def migrate(cr, version):
    """Set English source values for the demo disease classifier."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    for xmlid, values in DISEASE_VALUES.items():
        disease = env.ref(f"hr_hospital.{xmlid}", raise_if_not_found=False)
        if disease:
            disease.with_context(lang="en_US").write(values)

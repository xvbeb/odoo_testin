{
    "name": "Hospital",
    "summary": "Лікарня, управління лікарями, пацієнтами та відвідуваннями",
    "version": "19.0.1.0.2",
    "category": "Human Resources",
    "author": "xvbeb",
    "license": "AGPL-3",
    "depends": ["base"],
    'images': [
        'static/description/icon.png'
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/hospital_disease_data.xml",
        "views/hospital_disease_views.xml",
        "views/hospital_doctor_views.xml",
        "views/hospital_patient_views.xml",
        "views/hospital_patient_visit_views.xml",
        "views/hr_hospital_menus.xml",
    ],
    "demo": [
        "demo/hospital_doctor_demo.xml",
        "demo/hospital_patient_demo.xml",
    ],
    "application": True,
    "installable": True,
}

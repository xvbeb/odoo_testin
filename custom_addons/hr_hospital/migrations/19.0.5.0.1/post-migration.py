from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Позначити стандартну категорію інтернів у вже встановлених базах."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    intern_category = env.ref(
        "hr_hospital.doctor_category_intern",
        raise_if_not_found=False,
    )
    if intern_category:
        intern_category.is_intern = True

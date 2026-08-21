# Hospital

## Advanced ver

./venv/bin/python odoo/odoo-bin -c config/odoo.conf --dev=reload,xml

./venv/bin/python odoo/odoo-bin -c config/odoo.conf \
  -d odooschool_first_project \
  -u hr_hospital

  ./venv/bin/python odoo/odoo-bin -c config/odoo.conf \
  -d odooschool_first_project \
  -u hr_hospital \
  --stop-after-init

  ./venv/bin/python odoo/odoo-bin -c config/odoo.conf \
  -d odooschool_first_project \
  -i hr_hospital \
  --with-demo


  ./venv/bin/python odoo/odoo-bin module force-demo \
  -c config/odoo.conf \
  -d odooschool_first_project

  # Розробка
./venv/bin/python odoo/odoo-bin -c config/odoo.conf --dev=reload,xml

# Оновлення після змінення коду
./venv/bin/python odoo/odoo-bin -c config/odoo.conf -u hr_hospital
Hospital Management
===================

``hr_hospital`` is an educational Odoo 19 application for managing a
hospital's doctors, patients, diseases, and patient visits.

Features
--------

* doctor profiles, qualifications, mentors, and interns;
* patient profiles and personal doctor history;
* planned, completed, and cancelled patient visits;
* hierarchical disease classifier and disease search panel;
* kanban, list, form, calendar, and reporting views;
* PDF doctor report with visit history and assigned patients;
* visit and disease reporting wizards;
* Ukrainian translation for the interface and disease classifier;
* role-based access for patients, interns, doctors, managers, and
  administrators.

Installation
------------

Add the module directory to ``addons_path``, update the Apps list, and install
the **Hospital** application. From the project root it can be installed with::

    ./venv/bin/python odoo/odoo-bin -c config/odoo.conf \
        -d odooschool_first_project -i hr_hospital --with-demo

To update an existing installation::

    ./venv/bin/python odoo/odoo-bin -c config/odoo.conf \
        -d odooschool_first_project -u hr_hospital --stop-after-init

Configuration
-------------

Assign one Hospital access level to each user under **Settings > Users**.
Link patient and medical staff users through the **System User** field in the
corresponding patient or doctor profile.

Testing
-------

Run the module test suite with::

    ./venv/bin/python odoo/odoo-bin -c config/odoo.conf \
        -d odooschool_first_project -u hr_hospital \
        --test-enable --test-tags /hr_hospital --stop-after-init

License
-------

This module is distributed under the AGPL-3 license.

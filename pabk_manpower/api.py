
import frappe
from frappe.utils import today, add_days

def create_job():
    company = frappe.db.get_value('Company', {'name': 'PT Puriasri Bhaktikarya'}, 'name') or frappe.db.get_value('Company', {}, 'name')
    dept = frappe.db.get_value('Department', {'department_name': 'IT'}, 'name') or frappe.db.get_value('Department', {}, 'name')
    desig = frappe.db.get_value('Designation', {'designation_name': 'Software Engineer'}, 'name') or frappe.db.get_value('Designation', {}, 'name')
    
    if not dept: dept = frappe.get_doc({'doctype': 'Department', 'department_name': 'IT', 'company': company}).insert().name
    if not desig: desig = frappe.get_doc({'doctype': 'Designation', 'designation_name': 'Software Engineer'}).insert().name

    jo = frappe.get_doc({
        'doctype': 'Job Opening',
        'job_title': 'Software Engineer (Test)',
        'company': company,
        'status': 'Open',
        'publish': 1,
        'posted_on': today(),
        'closes_on': add_days(today(), 30),
        'department': dept,
        'designation': desig,
        'description': 'Testing Job Board.',
        'planned_vacancies': 1
    })
    jo.insert(ignore_permissions=True)
    frappe.db.commit()
    print('JOB_CREATED_SUCCESSFULLY:', jo.name)


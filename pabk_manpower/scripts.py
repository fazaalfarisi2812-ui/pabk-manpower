
import frappe
from frappe.utils import today, add_days

def create():
    company = frappe.db.get_value('Company', {'name': 'PT Puriasri Bhaktikarya'}, 'name')
    jo = frappe.get_doc({
        'doctype': 'Job Opening',
        'job_title': 'Software Engineer (Test)',
        'company': company,
        'status': 'Open',
        'publish': 1,
        'posted_on': today(),
        'closes_on': add_days(today(), 30),
        'description': 'Testing Job Board.'
    })
    jo.insert(ignore_permissions=True)
    frappe.db.commit()
    print('SUCCESS')


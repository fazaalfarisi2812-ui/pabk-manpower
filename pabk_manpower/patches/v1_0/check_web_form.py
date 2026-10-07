
import frappe
def execute():
    try:
        wf = frappe.get_doc('Web Form', 'job-opportunity')
        print(f'Exists in Frappe cache/DB! Name: {wf.name}, Route: {wf.route}, Published: {wf.published}')
        print(f'Is standard: {wf.is_standard}')
        print(f'Module: {wf.module}')
    except Exception as e:
        import traceback
        traceback.print_exc()


import frappe

def execute():
    try:
        from frappe.custom.doctype.property_setter.property_setter import make_property_setter
        make_property_setter("Job Opening", "route", "unique", 1, "Check")
        frappe.db.commit()
        print('Made route field unique in Job Opening')
    except Exception as e:
        import traceback
        traceback.print_exc()

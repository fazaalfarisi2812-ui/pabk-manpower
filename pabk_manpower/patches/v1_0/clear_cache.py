
import frappe
def execute():
    try:
        from frappe.website.utils import clear_cache
        clear_cache()
        frappe.db.commit()
        print('Cleared website cache.')
    except Exception as e:
        import traceback
        traceback.print_exc()

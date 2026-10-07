
import frappe
def execute():
    try:
        from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
        custom_fields = {
            "Job Opening": [
                {
                    "fieldname": "route",
                    "fieldtype": "Data",
                    "label": "Route",
                    "insert_after": "job_title",
                    "read_only": 0,
                    "default": ""
                },
                {
                    "fieldname": "published",
                    "fieldtype": "Check",
                    "label": "Published on Website",
                    "insert_after": "route",
                    "default": "0"
                }
            ]
        }
        create_custom_fields(custom_fields, ignore_validate=True)
        frappe.db.commit()
        print('Created Job Opening custom fields (route, published)')
    except Exception as e:
        import traceback
        traceback.print_exc()

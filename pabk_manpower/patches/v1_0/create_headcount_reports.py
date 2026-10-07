import frappe


def execute():
    """Create Headcount Planning script reports"""
    
    # Script Report: Headcount Plan vs Actual
    if not frappe.db.exists("Report", "Headcount Plan vs Actual"):
        report = frappe.get_doc({
            "doctype": "Report",
            "report_name": "Headcount Plan vs Actual",
            "module": "PABK Manpower",
            "report_type": "Script Report",
            "is_standard": "Yes",
            "ref_doctype": "Headcount Plan",
            "roles": [{"role": "System Manager"}],
            "script": "import frappe\n\ndef execute(filters=None):\n    columns = [\n        {\"label\": \"Department\", \"fieldname\": \"department\", \"fieldtype\": \"Link\", \"options\": \"Department\", \"width\": 200},\n        {\"label\": \"Planned Headcount\", \"fieldname\": \"planned_headcount\", \"fieldtype\": \"Int\", \"width\": 150},\n        {\"label\": \"Actual Headcount\", \"fieldname\": \"actual_headcount\", \"fieldtype\": \"Int\", \"width\": 150},\n        {\"label\": \"Variance\", \"fieldname\": \"variance\", \"fieldtype\": \"Int\", \"width\": 150},\n    ]\n    \n    data = frappe.db.sql(\"""\n        SELECT \n            department,\n            SUM(planned_headcount) as planned_headcount,\n            SUM(actual_headcount) as actual_headcount,\n            SUM(variance) as variance\n        FROM `tabHeadcount Plan`\n        WHERE docstatus = 1\n        GROUP BY department\n    \""", as_dict=True)\n    \n    return columns, data",
            "is_public": 1
        })
        report.insert(ignore_permissions=True)
        print("Created Report: Headcount Plan vs Actual")
    
    # Script Report: Headcount Cost Variance
    if not frappe.db.exists("Report", "Headcount Cost Variance"):
        report = frappe.get_doc({
            "doctype": "Report",
            "report_name": "Headcount Cost Variance",
            "module": "PABK Manpower",
            "report_type": "Script Report",
            "is_standard": "Yes",
            "ref_doctype": "Headcount Plan",
            "roles": [{"role": "System Manager"}],
            "script": "import frappe\n\ndef execute(filters=None):\n    columns = [\n        {\"label\": \"Department\", \"fieldname\": \"department\", \"fieldtype\": \"Link\", \"options\": \"Department\", \"width\": 200},\n        {\"label\": \"Total Budget\", \"fieldname\": \"total_budget\", \"fieldtype\": \"Currency\", \"width\": 150},\n        {\"label\": \"Actual Cost\", \"fieldname\": \"actual_cost\", \"fieldtype\": \"Currency\", \"width\": 150},\n        {\"label\": \"Cost Variance\", \"fieldname\": \"cost_variance\", \"fieldtype\": \"Currency\", \"width\": 150},\n    ]\n    \n    data = frappe.db.sql(\"""\n        SELECT \n            department,\n            SUM(total_budget) as total_budget,\n            SUM(actual_cost) as actual_cost,\n            SUM(cost_variance) as cost_variance\n        FROM `tabHeadcount Plan`\n        WHERE docstatus = 1\n        GROUP BY department\n    \""", as_dict=True)\n    \n    return columns, data",
            "is_public": 1
        })
        report.insert(ignore_permissions=True)
        print("Created Report: Headcount Cost Variance")
    
    frappe.db.commit()
    print("Script reports created")
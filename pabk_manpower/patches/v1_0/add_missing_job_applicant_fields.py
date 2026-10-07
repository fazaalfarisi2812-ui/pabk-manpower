import frappe

def execute():
    custom_fields = [
        {
            "doctype": "Custom Field",
            "dt": "Job Applicant",
            "fieldname": "portfolio_url",
            "label": "Portfolio/Website",
            "fieldtype": "Data",
            "insert_after": "linkedin_url"
        },
        {
            "doctype": "Custom Field",
            "dt": "Job Applicant",
            "fieldname": "expected_salary",
            "label": "Expected Salary (Monthly)",
            "fieldtype": "Currency",
            "insert_after": "portfolio_url"
        },
        {
            "doctype": "Custom Field",
            "dt": "Job Applicant",
            "fieldname": "notice_period",
            "label": "Notice Period (Days)",
            "fieldtype": "Int",
            "insert_after": "expected_salary"
        },
        {
            "doctype": "Custom Field",
            "dt": "Job Applicant",
            "fieldname": "source_channel",
            "label": "Source Channel",
            "fieldtype": "Select",
            "options": "LinkedIn\nJob Board\nReferral\nCompany Website\nRecruitment Agency\nWalk-in\nOther",
            "insert_after": "notice_period"
        }
    ]
    
    for cf in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": cf["dt"], "fieldname": cf["fieldname"]}):
            frappe.get_doc(cf).insert(ignore_permissions=True)
            print("Created custom field: " + cf["fieldname"])
        else:
            print("Custom field already exists: " + cf["fieldname"])
    
    frappe.db.commit()
    print("Done")
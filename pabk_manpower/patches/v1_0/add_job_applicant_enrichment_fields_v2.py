import frappe

def execute():
    fields = [
        {
            "fieldname": "linkedin_profile",
            "label": "LinkedIn Profile",
            "fieldtype": "Data",
            "insert_after": "email_id"
        },
        {
            "fieldname": "portfolio_url",
            "label": "Portfolio/Website",
            "fieldtype": "Data",
            "insert_after": "linkedin_profile"
        },
        {
            "fieldname": "expected_salary",
            "label": "Expected Salary (Monthly)",
            "fieldtype": "Currency",
            "insert_after": "portfolio_url"
        },
        {
            "fieldname": "notice_period",
            "label": "Notice Period (Days)",
            "fieldtype": "Int",
            "insert_after": "expected_salary"
        },
        {
            "fieldname": "source_channel",
            "label": "Source Channel",
            "fieldtype": "Select",
            "options": "Job Board\nLinkedIn\nReferral\nCompany Website\nWalk-in\nAgency\nOther",
            "insert_after": "notice_period"
        }
    ]

    for field in fields:
        if not frappe.db.exists("Custom Field", f"Job Applicant-{field['fieldname']}"):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Job Applicant",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", ""),
                "insert_after": field["insert_after"]
            }).insert(ignore_permissions=True)
            print(f"Created custom field: {field['fieldname']}")
        else:
            print(f"Custom field exists: {field['fieldname']}")

    frappe.db.commit()
    print("Job Applicant enrichment fields done")
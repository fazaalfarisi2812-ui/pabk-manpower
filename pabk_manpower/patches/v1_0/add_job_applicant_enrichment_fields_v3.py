import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
        "Job Applicant": [
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
    }
    
    create_custom_fields(custom_fields)
    print("Job Applicant enrichment fields created via API")
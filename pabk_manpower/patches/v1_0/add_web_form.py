
import frappe
def execute():
    try:
        if frappe.db.exists('Web Form', 'job-opportunity'):
            frappe.delete_doc('Web Form', 'job-opportunity', ignore_permissions=True)
            frappe.db.commit()
            print('Deleted existing job-opportunity')
        
        doc = frappe.get_doc({
            "doctype": "Web Form",
            "name": "job-opportunity-form",
            "title": "Job Opportunity",
            "route": "job-opportunity",
            "doc_type": "Job Applicant",
            "is_standard": 1,
            "module": "PABK Manpower",
            "published": 1,
            "login_required": 0,
            "allow_multiple": 1,
            "allow_edit": 0,
            "show_attachments": 1,
            "success_message": "Thank you for applying. We will review your application and get back to you shortly.",
            "success_url": "/job-opportunities",
            "web_form_fields": [
                {"fieldname": "job_title", "fieldtype": "Data", "label": "Job Title", "reqd": 1, "hidden": 1},
                {"fieldname": "applicant_name", "fieldtype": "Data", "label": "Full Name", "reqd": 1},
                {"fieldname": "email_id", "fieldtype": "Data", "label": "Email", "reqd": 1},
                {"fieldname": "phone_number", "fieldtype": "Data", "label": "Phone Number", "reqd": 1},
                {"fieldname": "linkedin_profile", "fieldtype": "Data", "label": "LinkedIn Profile"},
                {"fieldname": "portfolio_url", "fieldtype": "Data", "label": "Portfolio/Website"},
                {"fieldname": "expected_salary", "fieldtype": "Currency", "label": "Expected Salary (Monthly)"},
                {"fieldname": "notice_period", "fieldtype": "Int", "label": "Notice Period (Days)"},
                {"fieldname": "source_channel", "fieldtype": "Select", "label": "How did you hear about us?", "options": "Job Board" + chr(10) + "LinkedIn" + chr(10) + "Referral" + chr(10) + "Company Website" + chr(10) + "Walk-in" + chr(10) + "Agency" + chr(10) + "Other"},
                {"fieldname": "resume_attachment", "fieldtype": "Attach", "label": "Resume/CV", "reqd": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print('Created Web Form: ' + doc.name)
    except Exception as e:
        import traceback
        traceback.print_exc()

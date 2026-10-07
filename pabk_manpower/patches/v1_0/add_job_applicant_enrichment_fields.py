# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe


def execute():
    """Add custom fields to Job Applicant for candidate enrichment"""
    
    custom_fields = {
        "Job Applicant": [
            {
                "fieldname": "linkedin_url",
                "fieldtype": "Data",
                "label": "LinkedIn URL",
                "insert_after": "resume_link",
                "options": "URL",
                "description": "LinkedIn profile URL for enrichment"
            },
            {
                "fieldname": "github_url",
                "fieldtype": "Data",
                "label": "GitHub URL",
                "insert_after": "linkedin_url",
                "options": "URL",
                "description": "GitHub profile URL for enrichment"
            },
            {
                "fieldname": "section_break_enrichment",
                "fieldtype": "Section Break",
                "label": "Enrichment Data",
                "insert_after": "github_url",
                "collapsible": 1
            },
            {
                "fieldname": "enriched_skills",
                "fieldtype": "Text",
                "label": "Enriched Skills",
                "insert_after": "section_break_enrichment",
                "read_only": 1,
                "description": "Auto-populated from LinkedIn/GitHub"
            },
            {
                "fieldname": "enriched_experience",
                "fieldtype": "Text",
                "label": "Enriched Experience",
                "insert_after": "enriched_skills",
                "read_only": 1,
                "description": "Auto-populated from LinkedIn/GitHub"
            },
            {
                "fieldname": "enrichment_status",
                "fieldtype": "Select",
                "label": "Enrichment Status",
                "insert_after": "enriched_experience",
                "options": "Pending\nIn Progress\nCompleted\nFailed",
                "default": "Pending",
                "read_only": 1
            },
            {
                "fieldname": "enrichment_date",
                "fieldtype": "Datetime",
                "label": "Last Enriched",
                "insert_after": "enrichment_status",
                "read_only": 1
            }
        ]
    }
    
    for doctype, fields in custom_fields.items():
        for field in fields:
            # Check if custom field already exists
            existing = frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]})
            if not existing:
                cf = frappe.get_doc({
                    "doctype": "Custom Field",
                    "dt": doctype,
                    **field
                })
                cf.insert(ignore_permissions=True)
                print(f"Created custom field: {doctype}.{field['fieldname']}")
            else:
                print(f"Custom field already exists: {doctype}.{field['fieldname']}")
    
    frappe.db.commit()


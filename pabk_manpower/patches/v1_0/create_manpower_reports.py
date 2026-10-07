# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
import json


def execute():
    """Create Manpower Reports"""
    
    reports_data = [
        {
            "doctype": "Report",
            "report_name": "Manpower Deployed vs Contracted",
            "report_type": "Script Report",
            "module": "PABK Manpower",
            "is_standard": "Yes",
            "roles": [
                {"role": "System Manager"},
                {"role": "Sales Manager"},
                {"role": "HR Manager"}
            ]
        },
        {
            "doctype": "Report",
            "report_name": "Site Billing vs Cost",
            "report_type": "Script Report",
            "module": "PABK Manpower",
            "is_standard": "Yes",
            "roles": [
                {"role": "System Manager"},
                {"role": "Sales Manager"},
                {"role": "HR Manager"}
            ]
        },
        {
            "doctype": "Report",
            "report_name": "Manpower Utilization Trend",
            "report_type": "Script Report",
            "module": "PABK Manpower",
            "is_standard": "Yes",
            "roles": [
                {"role": "System Manager"},
                {"role": "Sales Manager"},
                {"role": "HR Manager"}
            ]
        }
    ]
    
    for report_data in reports_data:
        if not frappe.db.exists("Report", report_data["report_name"]):
            report = frappe.get_doc(report_data)
            report.insert(ignore_permissions=True)
            print(f"Created report: {report_data['report_name']}")
        else:
            print(f"Report already exists: {report_data['report_name']}")


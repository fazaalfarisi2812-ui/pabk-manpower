# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, add_days, date_diff, flt
from frappe import _


def daily():
    """Daily scheduled tasks"""
    generate_pending_invoices()


def generate_pending_invoices():
    """Generate invoices for approved timesheets that don't have invoices yet"""
    # Find submitted timesheets without invoices
    timesheets = frappe.get_all("Timesheet", 
        filters={
            "docstatus": 1,
            "custom_manpower_contract": ["!=", ""],
            "status": "Submitted"
        },
        fields=["name", "custom_manpower_contract", "employee", "total_hours"]
    )
    
    for ts in timesheets:
        # Check if invoice already exists
        existing = frappe.db.exists("Sales Invoice", {"timesheet": ts.name, "docstatus": ["!=", 2]})
        if not existing:
            # Trigger the on_submit logic manually
            doc = frappe.get_doc("Timesheet", ts.name)
            # Import and call the function
            from pabk_manpower.pabk_manpower.doctype.manpower_contract.manpower_contract import on_timesheet_submit
            try:
                on_timesheet_submit(doc, "scheduled")
            except Exception as e:
                frappe.log_error(f"Failed to generate invoice for Timesheet {ts.name}: {e}", "Manpower Invoice Generation")


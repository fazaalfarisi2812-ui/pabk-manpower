# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, add_days, date_diff


class ManpowerContract(Document):
    def validate(self):
        self.set_deployed_count()
        self.validate_dates()
    
    def on_submit(self):
        self.set_deployed_count()
    
    def on_cancel(self):
        self.set_deployed_count()
    
    def validate_dates(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            frappe.throw("End Date cannot be before Start Date")
    
    def set_deployed_count(self):
        """Calculate currently deployed headcount from active shift assignments"""
        deployed = frappe.db.count("Manpower Shift Assignment", {
            "contract": self.name,
            "status": "Active"
        })
        self.db_set("deployed_count", deployed, update_modified=False)
        
        # Also update site totals
        if self.site:
            self.update_site_totals()
    
    def update_site_totals(self):
        """Update contracted and deployed headcount on the site"""
        site = frappe.get_doc("Manpower Site", self.site)
        
        # Calculate contracted headcount from active contracts at this site
        contracted = frappe.db.sql("""
            SELECT SUM(headcount) FROM `tabManpower Contract`
            WHERE site = %s AND status = 'Active' AND docstatus = 1
        """, (self.site,))[0][0] or 0
        
        # Calculate deployed headcount from active shift assignments at this site
        deployed = frappe.db.sql("""
            SELECT COUNT(*) FROM `tabManpower Shift Assignment` msa
            JOIN `tabManpower Contract` mc ON msa.contract = mc.name
            WHERE mc.site = %s AND msa.status = 'Active' AND msa.docstatus = 1
        """, (self.site,))[0][0] or 0
        
        site.db_set("contracted_headcount", contracted, update_modified=False)
        site.db_set("deployed_headcount", deployed, update_modified=False)
    
    @frappe.whitelist()
    def get_utilization_pct(self):
        """Get utilization percentage for dashboard"""
        if not self.headcount:
            return 0
        return flt(self.deployed_count / self.headcount * 100, 2)
    
    @frappe.whitelist()
    def get_billing_vs_cost(self):
        """Get billing vs cost comparison for dashboard"""
        # Calculate based on active shift assignments
        assignments = frappe.get_all("Manpower Shift Assignment",
            filters={"contract": self.name, "status": "Active", "docstatus": 1},
            fields=["employee", "billing_rate", "cost_rate"]
        )
        
        total_billing = sum(flt(a.billing_rate) for a in assignments)
        total_cost = sum(flt(a.cost_rate) for a in assignments)
        
        return {
            "billing": total_billing,
            "cost": total_cost,
            "margin": total_billing - total_cost,
            "margin_pct": flt((total_billing - total_cost) / total_billing * 100, 2) if total_billing else 0
        }


@frappe.whitelist()
def on_timesheet_submit(doc, method):
    """Hook: Auto-create Draft Sales Invoice from Timesheet based on Manpower Contract"""
    if not doc.custom_manpower_contract:
        return
    
    contract = frappe.get_doc("Manpower Contract", doc.custom_manpower_contract)
    if contract.status != "Active":
        return
    
    # Check if invoice already exists for this timesheet
    existing = frappe.db.exists("Sales Invoice", {"timesheet": doc.name, "docstatus": ["!=", 2]})
    if existing:
        return
    
    # Create Sales Invoice
    si = frappe.new_doc("Sales Invoice")
    si.customer = contract.client
    si.due_date = add_days(frappe.utils.today(), 30)
    si.project = contract.site
    
    # Calculate billing amount: hours * rate * (1 + markup%)
    # Use timesheets child table (ERPNext standard) for traceability
    markup = flt(contract.markup_pct) / 100
    overtime_multiplier = flt(contract.overtime_multiplier) or 1.5
    
    for ts_detail in doc.time_logs:
        if ts_detail.billing_hours:
            rate = ts_detail.billing_rate or 0
            billing_rate = rate * (1 + markup)
            
            # Calculate overtime if applicable
            hours = flt(ts_detail.billing_hours)
            ot_hours = 0
            if contract.shift_template:
                shift = frappe.get_doc("Shift Type", contract.shift_template)
                if shift.working_hours_threshold_for_half_day and hours > shift.working_hours_threshold_for_half_day:
                    # Use shift threshold as overtime threshold
                    threshold = shift.working_hours_threshold_for_half_day
                else:
                    threshold = 8  # default 8 hours
            else:
                threshold = 8
            
            if hours > threshold:
                ot_hours = hours - threshold
                hours = threshold
            
            si.append("timesheets", {
                "time_sheet": doc.name,
                "timesheet_detail": ts_detail.name,
                "activity_type": ts_detail.activity_type,
                "description": f"{ts_detail.activity_type} - {ts_detail.from_time} to {ts_detail.to_time}",
                "from_time": ts_detail.from_time,
                "to_time": ts_detail.to_time,
                "billing_hours": hours,
                "billing_amount": flt(hours) * billing_rate,
            })
            
            # Add overtime as separate line if applicable
            if ot_hours > 0:
                ot_rate = billing_rate * overtime_multiplier
                si.append("timesheets", {
                    "time_sheet": doc.name,
                    "timesheet_detail": ts_detail.name,
                    "activity_type": f"{ts_detail.activity_type} (Lembur)",
                    "description": f"{ts_detail.activity_type} (Lembur) - {ts_detail.from_time} to {ts_detail.to_time}",
                    "from_time": ts_detail.from_time,
                    "to_time": ts_detail.to_time,
                    "billing_hours": ot_hours,
                    "billing_amount": flt(ot_hours) * ot_rate,
                })
    
    si.set_missing_values()
    si.insert(ignore_permissions=True)
    
    # Optionally auto-submit
    if contract.auto_submit_invoice:
        si.submit()
        frappe.msgprint(f"Sales Invoice {si.name} created and submitted for Timesheet {doc.name}")
    else:
        frappe.msgprint(f"Draft Sales Invoice {si.name} created for Timesheet {doc.name}")


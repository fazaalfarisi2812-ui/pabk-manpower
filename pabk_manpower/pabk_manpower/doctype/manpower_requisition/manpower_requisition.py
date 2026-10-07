# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime


class ManpowerRequisition(Document):
    def validate(self):
        if self.required_date and getdate(self.required_date) < getdate():
            frappe.msgprint("Required date is in the past", alert=True)

    def on_submit(self):
        if self.status != "Approved":
            frappe.throw("Only Approved requisitions can be submitted")
        
        # Create Job Opening
        self.create_job_opening()

    def create_job_opening(self):
        if self.linked_job_opening:
            return
        
        jo = frappe.new_doc("Job Opening")
        jo.job_title = self.position
        jo.company = frappe.defaults.get_user_default("Company")
        jo.status = "Open"
        jo.no_of_openings = self.headcount_required
        jo.employment_type = self.employment_type
        jo.job_description = self.job_description
        jo.description = self.requirements
        jo.custom_manpower_requisition = self.name
        
        if self.min_salary and self.max_salary:
            jo.lower_range = self.min_salary
            jo.upper_range = self.max_salary
        
        jo.insert(ignore_permissions=True)
        jo.submit()
        
        self.db_set("linked_job_opening", jo.name)
        frappe.msgprint(f"Job Opening {jo.name} created")


@frappe.whitelist()
def on_update(doc, method):
    """Auto-update linked Job Opening when requisition changes"""
    if doc.linked_job_opening and doc.status == "Approved":
        jo = frappe.get_doc("Job Opening", doc.linked_job_opening)
        jo.job_title = doc.position
        jo.no_of_openings = doc.headcount_required
        jo.employment_type = doc.employment_type
        jo.job_description = doc.job_description
        jo.description = doc.requirements
        if doc.min_salary:
            jo.lower_range = doc.min_salary
        if doc.max_salary:
            jo.upper_range = doc.max_salary
        jo.save(ignore_permissions=True)

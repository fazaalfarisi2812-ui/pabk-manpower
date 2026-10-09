# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate, nowdate, cstr
from datetime import datetime
import json

class BPJSCompliance(Document):
    def validate(self):
        self.set_calculated_amounts()
        self.validate_bpjs_amounts()
    
    def set_calculated_amounts(self):
        """Calculate BPJS amounts based on employee contract"""
        if not self.employee or not self.contract:
            return
        
        # Get employee and contract data
        employee = frappe.get_doc("Employee", self.employee)
        contract = frappe.get_doc("Manpower Contract", self.contract)
        
        # Calculate BPJS Kesehatan (based on salary)
        salary = employee.salary or 0
        self.bpjs_kesehatan_employee_share = flt(salary * 0.01)  # 1% employee
        self.bpjs_kesehatan_employer_share = flt(salary * 0.04)  # 4% employer
        
        # Calculate BPJS Ketenagakerjaan (based on salary)
        self.bpjs_ketenagakerjaan_jht_employee = flt(salary * 0.02)  # 2% employee
        self.bpjs_ketenagakerjaan_jht_employer = flt(salary * 0.037)  # 3.7% employer
        
        self.bpjs_ketenagakerjaan_jp_employee = flt(salary * 0.01)  # 1% employee
        self.bpjs_ketenagakerjaan_jp_employer = flt(salary * 0.02)  # 2% employer
        
        # Calculate JKK (based on occupational risk)
        if contract.job_type == "High Risk":
            jkk_rate = 0.0174
        elif contract.job_type == "Medium Risk":
            jkk_rate = 0.009
        else:
            jkk_rate = 0.0024
        
        self.bpjs_ketenagakerjaan_jkk_employer = flt(salary * jkk_rate)
        
        # Calculate JKM (based on age)
        if employee.age > 45:
            jkm_rate = 0.003
        else:
            jkm_rate = 0.002
        
        self.bpjs_ketenagakerjaan_jkm_employer = flt(salary * jkm_rate)
        
        # Calculate totals
        self.total_employee_share = flt(
            self.bpjs_kesehatan_employee_share +
            self.bpjs_ketenagakerjaan_jht_employee +
            self.bpjs_ketenagakerjaan_jp_employee
        )
        
        self.total_employer_share = flt(
            self.bpjs_kesehatan_employer_share +
            self.bpjs_ketenagakerjaan_jht_employer +
            self.bpjs_ketenagakerjaan_jp_employer +
            self.bpjs_ketenagakerjaan_jkk_employer +
            self.bpjs_ketenagakerjaan_jkm_employer
        )
        
        self.total_bpjs = flt(self.total_employee_share + self.total_employer_share)
    
    def validate_bpjs_amounts(self):
        """Validate that amounts are reasonable"""
        if self.total_employee_share > 500000:  # Max 500k/month
            frappe.throw("Employee BPJS share cannot exceed IDR 500,000 per month")
        
        if self.total_employer_share > 2000000:  # Max 2M/month
            frappe.throw("Employer BPJS share cannot exceed IDR 2,000,000 per month")


@frappe.whitelist()
def calculate_bpjs_for_employee(employee_id, month, year):
    """Helper function to calculate BPJS for an employee in a specific month"""
    # Check if BPJS already calculated for this month
    existing = frappe.db.exists("BPJS Compliance", {
        "employee": employee_id,
        "month": month,
        "status": ["in", ["Submitted", "Paid"]]
    })
    
    if existing:
        return None
    
    # Create BPJS compliance record
    bpjs = frappe.new_doc("BPJS Compliance")
    bpjs.employee = employee_id
    bpjs.month = month
    bpjs.status = "Calculated"
    
    # Auto-fill contract from employee
    employee = frappe.get_doc("Employee", employee_id)
    if employee.manpower_contract:
        bpjs.contract = employee.manpower_contract
    
    # Calculate amounts
    bpjs.set_calculated_amounts()
    
    # Insert without submission
    bpjs.insert(ignore_permissions=True)
    
    return bpjs.name


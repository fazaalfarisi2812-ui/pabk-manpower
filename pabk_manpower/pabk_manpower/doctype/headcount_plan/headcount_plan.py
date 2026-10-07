# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, cint


class HeadcountPlan(Document):
    def validate(self):
        self.calculate_variance()
        self.calculate_cost_variance()
    
    def calculate_variance(self):
        """Calculate headcount variance"""
        self.variance = cint(self.actual_headcount) - cint(self.planned_headcount)
    
    def calculate_cost_variance(self):
        """Calculate cost variance"""
        self.cost_variance = flt(self.actual_cost) - flt(self.total_budget)
    
    def on_submit(self):
        """Update actual headcount from active employees"""
        self.update_actual_headcount()
        self.update_actual_cost()
        self.calculate_variance()
        self.calculate_cost_variance()
    
    def update_actual_headcount(self):
        """Count active employees in this department"""
        if not self.department:
            return
        
        count = frappe.db.count("Employee", {
            "department": self.department,
            "status": "Active"
        })
        self.actual_headcount = count
    
    def update_actual_cost(self):
        """Sum salary components for active employees in department"""
        if not self.department:
            return
        
        employees = frappe.get_all("Employee", 
            filters={"department": self.department, "status": "Active"},
            fields=["name"]
        )
        
        total = 0
        for emp in employees:
            # Get latest salary structure assignment
            ssa = frappe.get_all("Salary Structure Assignment",
                filters={"employee": emp.name, "docstatus": 1},
                fields=["base"],
                order_by="from_date desc",
                limit=1
            )
            if ssa:
                total += flt(ssa[0].base)
        
        self.actual_cost = total


@frappe.whitelist()
def get_headcount_vs_actual(fiscal_year=None, department=None):
    """API for dashboard: returns headcount plan vs actual data"""
    filters = {}
    if fiscal_year:
        filters["fiscal_year"] = fiscal_year
    if department:
        filters["department"] = department
    
    plans = frappe.get_all("Headcount Plan",
        filters=filters,
        fields=["plan_name", "fiscal_year", "department", 
                "planned_headcount", "actual_headcount", "variance",
                "total_budget", "actual_cost", "cost_variance", "status"],
        order_by="fiscal_year desc, department"
    )
    
    return plans


@frappe.whitelist()
def sync_from_manpower_requisitions(fiscal_year):
    """Create/update headcount plans from approved Manpower Requisitions"""
    requisitions = frappe.get_all("Manpower Requisition",
        filters={"status": "Approved", "docstatus": 1},
        fields=["department", "position", "headcount_required", "min_salary", "max_salary"]
    )
    
    # Group by department
    dept_data = {}
    for req in requisitions:
        dept = req.department
        if dept not in dept_data:
            dept_data[dept] = {"headcount": 0, "budget": 0}
        dept_data[dept]["headcount"] += cint(req.headcount_required)
        # Use max salary for budget
        dept_data[dept]["budget"] += flt(req.max_salary or req.min_salary) * cint(req.headcount_required)
    
    created = 0
    for dept, data in dept_data.items():
        # Check if plan exists
        existing = frappe.get_all("Headcount Plan",
            filters={"fiscal_year": fiscal_year, "department": dept},
            limit=1
        )
        
        if existing:
            plan = frappe.get_doc("Headcount Plan", existing[0].name)
        else:
            plan = frappe.new_doc("Headcount Plan")
            plan.fiscal_year = fiscal_year
            plan.department = dept
            plan.plan_name = f"Headcount Plan {fiscal_year} - {dept}"
        
        plan.planned_headcount = data["headcount"]
        plan.total_budget = data["budget"]
        plan.status = "Draft"
        plan.save(ignore_permissions=True)
        created += 1
    
    frappe.db.commit()
    return {"created": created, "message": f"Synced {created} department plans from requisitions"}

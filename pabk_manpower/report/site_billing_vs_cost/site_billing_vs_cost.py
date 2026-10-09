# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        _("Site") + ":Link/Manpower Site:200",
        _("Total Billing") + ":Currency:150",
        _("Total Cost") + ":Currency:150",
        _("Margin") + ":Currency:150",
        _("Margin %") + ":Percent:100"
    ]


def get_data():
    data = []
    
    sites = frappe.get_all("Manpower Site",
        filters={"status": "Active"},
        fields=["name", "site_name"]
    )
    
    for site in sites:
        # Get all active contracts at this site
        contracts = frappe.get_all("Manpower Contract",
            filters={"site": site.name, "status": "Active", "docstatus": 1},
            fields=["name"]
        )
        
        total_billing = 0
        total_cost = 0
        
        for contract in contracts:
            # Get active shift assignments for this contract
            assignments = frappe.get_all("Manpower Shift Assignment",
                filters={"contract": contract.name, "status": "Active", "docstatus": 1},
                fields=["billing_rate", "cost_rate"]
            )
            
            for a in assignments:
                total_billing += flt(a.billing_rate)
                total_cost += flt(a.cost_rate)
        
        margin = total_billing - total_cost
        margin_pct = flt(margin / total_billing * 100, 2) if total_billing else 0
        
        data.append({
            "site": site.name,
            "total_billing": total_billing,
            "total_cost": total_cost,
            "margin": margin,
            "margin_pct": margin_pct
        })
    
    return data

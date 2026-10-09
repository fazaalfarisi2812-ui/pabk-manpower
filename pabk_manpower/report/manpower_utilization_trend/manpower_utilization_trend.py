# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, add_days, date_diff, flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    cols = [_("Date") + ":Date:100"]
    
    # Add columns for each site
    sites = frappe.get_all("Manpower Site", filters={"status": "Active"}, fields=["name", "site_name"])
    for site in sites:
        cols.append(_(site.site_name) + " Utilization %" + ":Percent:120")
    
    return cols


def get_data(filters):
    # Default to last 30 days
    to_date = getdate(filters.get("to_date")) if filters and filters.get("to_date") else getdate()
    from_date = getdate(filters.get("from_date")) if filters and filters.get("from_date") else add_days(to_date, -30)
    
    sites = frappe.get_all("Manpower Site", filters={"status": "Active"}, fields=["name", "site_name"])
    
    data = []
    current_date = from_date
    
    while current_date <= to_date:
        row = {"date": current_date}
        
        for site in sites:
            # Get active contracts at this site as of this date
            contracts = frappe.db.sql("""
                SELECT name, headcount FROM `tabManpower Contract`
                WHERE site = %s AND status = 'Active' AND docstatus = 1
                AND start_date <= %s AND (end_date IS NULL OR end_date >= %s)
            """, (site.name, current_date, current_date), as_dict=True)
            
            total_contracted = sum(c.headcount for c in contracts)
            
            if total_contracted == 0:
                row[site.site_name + " Utilization %"] = 0
                continue
            
            # Get deployed count from shift assignments
            deployed = frappe.db.sql("""
                SELECT COUNT(*) FROM `tabManpower Shift Assignment` msa
                JOIN `tabManpower Contract` mc ON msa.contract = mc.name
                WHERE mc.site = %s AND msa.status = 'Active' AND msa.docstatus = 1
                AND msa.start_date <= %s AND (msa.end_date IS NULL OR msa.end_date >= %s)
            """, (site.name, current_date, current_date))[0][0] or 0
            
            utilization = flt(deployed / total_contracted * 100, 2)
            row[site.site_name + " Utilization %"] = utilization
        
        data.append(row)
        current_date = add_days(current_date, 1)
    
    return data

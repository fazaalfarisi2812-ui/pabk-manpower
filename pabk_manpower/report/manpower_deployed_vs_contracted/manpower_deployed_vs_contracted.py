# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data()
    return columns, data


def get_columns():
    return [
        _("Site") + ":Link/Manpower Site:200",
        _("Contracted Headcount") + ":Int:150",
        _("Deployed Headcount") + ":Int:150",
        _("Utilization %") + ":Percent:120",
        _("Status") + "::100"
    ]


def get_data():
    data = []
    
    sites = frappe.get_all("Manpower Site",
        filters={"status": "Active"},
        fields=["name", "site_name", "contracted_headcount", "deployed_headcount", "status"]
    )
    
    for site in sites:
        contracted = site.contracted_headcount or 0
        deployed = site.deployed_headcount or 0
        utilization = (deployed / contracted * 100) if contracted else 0
        
        data.append({
            "site": site.name,
            "contracted_headcount": contracted,
            "deployed_headcount": deployed,
            "utilization_pct": utilization,
            "status": site.status
        })
    
    return data

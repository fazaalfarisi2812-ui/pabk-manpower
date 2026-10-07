# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
import json


def execute():
    """Create Manpower Utilization Dashboard with charts and cards"""
    
    # Create charts first
    charts_data = [
        {
            "doctype": "Dashboard Chart",
            "chart_name": "Deployed vs Contracted Headcount",
            "chart_type": "Report",
            "report_name": "Manpower Deployed vs Contracted",
            "type": "Bar",
            "is_standard": 1,
            "module": "PABK Manpower",
            "filters_json": "{}",
            "timeseries": 0
        },
        {
            "doctype": "Dashboard Chart",
            "chart_name": "Billing vs Cost per Site",
            "chart_type": "Report",
            "report_name": "Site Billing vs Cost",
            "type": "Bar",
            "is_standard": 1,
            "module": "PABK Manpower",
            "filters_json": "{}",
            "timeseries": 0
        },
        {
            "doctype": "Dashboard Chart",
            "chart_name": "Active Contracts",
            "chart_type": "Count",
            "document_type": "Manpower Contract",
            "filters_json": "{\"status\": \"Active\"}",
            "type": "Bar",
            "is_standard": 1,
            "module": "PABK Manpower",
            "timeseries": 0
        },
        {
            "doctype": "Dashboard Chart",
            "chart_name": "Open Requisitions",
            "chart_type": "Count",
            "document_type": "Manpower Requisition",
            "filters_json": "{\"status\": \"Open\"}",
            "type": "Bar",
            "is_standard": 1,
            "module": "PABK Manpower",
            "timeseries": 0
        },
        {
            "doctype": "Dashboard Chart",
            "chart_name": "Utilization Trend (30 Days)",
            "chart_type": "Report",
            "report_name": "Manpower Utilization Trend",
            "type": "Line",
            "is_standard": 1,
            "module": "PABK Manpower",
            "filters_json": "{}",
            "timeseries": 1
        }
    ]
    
    for chart_data in charts_data:
        if not frappe.db.exists("Dashboard Chart", chart_data["chart_name"]):
            chart = frappe.get_doc(chart_data)
            chart.insert(ignore_permissions=True)
            print(f"Created chart: {chart_data['chart_name']}")
        else:
            print(f"Chart already exists: {chart_data['chart_name']}")
    
    # Create number cards
    cards_data = [
        {
            "doctype": "Number Card",
            "label": "Total Deployed",
            "type": "Document Type",
            "document_type": "Manpower Shift Assignment",
            "function": "Count",
            "filters_json": "{\"status\": \"Active\"}",
            "is_standard": 1,
            "module": "PABK Manpower"
        },
        {
            "doctype": "Number Card",
            "label": "Total Contracted",
            "type": "Document Type",
            "document_type": "Manpower Contract",
            "function": "Sum",
            "aggregate_function_based_on": "headcount",
            "filters_json": "{\"status\": \"Active\"}",
            "is_standard": 1,
            "module": "PABK Manpower"
        }
    ]
    
    for card_data in cards_data:
        if not frappe.db.exists("Number Card", card_data["label"]):
            card = frappe.get_doc(card_data)
            card.insert(ignore_permissions=True)
            print(f"Created card: {card_data['label']}")
        else:
            print(f"Card already exists: {card_data['label']}")
    
    # Create dashboard
    if not frappe.db.exists("Dashboard", "Manpower Utilization"):
        dashboard = frappe.new_doc("Dashboard")
        dashboard.dashboard_name = "Manpower Utilization"
        dashboard.module = "PABK Manpower"
        dashboard.is_standard = 1
        dashboard.is_default = 0
        
        # Add charts
        charts_list = [
            {"chart": "Deployed vs Contracted Headcount", "width": "Half"},
            {"chart": "Billing vs Cost per Site", "width": "Half"},
            {"chart": "Active Contracts", "width": "Half"},
            {"chart": "Open Requisitions", "width": "Half"},
            {"chart": "Utilization Trend (30 Days)", "width": "Full"}
        ]
        
        for chart in charts_list:
            dashboard.append("charts", chart)
        
        # Add number cards
        cards_list = [
            {"card": "Total Deployed"},
            {"card": "Total Contracted"}
        ]
        
        for card in cards_list:
            dashboard.append("cards", card)
        
        dashboard.insert(ignore_permissions=True)
        print("Manpower Utilization Dashboard created")
    else:
        print("Dashboard already exists: Manpower Utilization")


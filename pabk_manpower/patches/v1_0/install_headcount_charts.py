import frappe


def execute():
    """Install Headcount Planning dashboard charts and number card"""
    
    # Dashboard Chart: Headcount Plan vs Actual (Report type)
    if not frappe.db.exists("Dashboard Chart", "Headcount Plan vs Actual"):
        chart = frappe.get_doc({
            "doctype": "Dashboard Chart",
            "chart_name": "Headcount Plan vs Actual",
            "module": "PABK Manpower",
            "chart_type": "Report",
            "report_name": "Headcount Plan vs Actual",
            "use_report_chart": 1,
            "filters_json": "{}",
            "is_public": 1,
            "is_standard": 1,
            "timeseries": 0,
            "refresh_interval": 0
        })
        chart.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Created: Headcount Plan vs Actual")
    
    # Dashboard Chart: Headcount Cost Variance (Report type)
    if not frappe.db.exists("Dashboard Chart", "Headcount Cost Variance"):
        chart = frappe.get_doc({
            "doctype": "Dashboard Chart",
            "chart_name": "Headcount Cost Variance",
            "module": "PABK Manpower",
            "chart_type": "Report",
            "report_name": "Headcount Cost Variance",
            "use_report_chart": 1,
            "filters_json": "{}",
            "is_public": 1,
            "is_standard": 1,
            "timeseries": 0,
            "refresh_interval": 0
        })
        chart.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Created: Headcount Cost Variance")
    
    # Number Card: Total Headcount Variance
    if not frappe.db.exists("Number Card", "Total Headcount Variance"):
        card = frappe.get_doc({
            "doctype": "Number Card",
            "label": "Total Headcount Variance",
            "module": "PABK Manpower",
            "document_type": "Headcount Plan",
            "function": "Sum",
            "aggregate_function_based_on": "variance",
            "filters_json": '{"docstatus": 1}',
            "format": "#,##0",
            "is_public": 1,
            "is_standard": 1
        })
        card.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Created: Total Headcount Variance")
    
    print("Charts and number card installed")
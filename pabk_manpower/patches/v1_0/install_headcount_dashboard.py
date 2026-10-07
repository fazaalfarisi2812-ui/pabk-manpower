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
        print("Created: Total Headcount Variance")
    
    # Workspace: Headcount Planning
    if not frappe.db.exists("Workspace", "Headcount Planning"):
        workspace = frappe.get_doc({
            "doctype": "Workspace",
            "name": "Headcount Planning",
            "module": "PABK Manpower",
            "label": "Headcount Planning",
            "icon": "users",
            "color": "#36a2eb",
            "is_standard": 1,
            "is_public": 1,
            "sequence_id": 10,
            "charts": [
                {"chart_name": "Headcount Plan vs Actual", "label": "Headcount Plan vs Actual"},
                {"chart_name": "Headcount Cost Variance", "label": "Headcount Cost Variance"}
            ],
            "number_cards": [
                {"number_card_name": "Total Headcount Variance", "label": "Total Headcount Variance"}
            ],
            "shortcuts": [
                {"label": "New Headcount Plan", "type": "DocType", "link_to": "Headcount Plan", "format": "New"},
                {"label": "Manpower Requisitions", "type": "DocType", "link_to": "Manpower Requisition"},
                {"label": "Job Openings", "type": "DocType", "link_to": "Job Opening"}
            ],
            "links": [
                {"label": "Headcount Plans", "type": "DocType", "link_to": "Headcount Plan", "icon": "users"},
                {"label": "Manpower Requisitions", "type": "DocType", "link_to": "Manpower Requisition", "icon": "clipboard-list"},
                {"label": "Employees", "type": "DocType", "link_to": "Employee", "icon": "id-badge"}
            ]
        })
        workspace.insert(ignore_permissions=True)
        print("Created: Headcount Planning workspace")
    
    frappe.db.commit()
    print("All dashboard artifacts installed")
import frappe


def execute():
    """Create Headcount Planning workspace"""
    
    if not frappe.db.exists("Workspace", "Headcount Planning"):
        workspace = frappe.get_doc({
            "doctype": "Workspace",
            "name": "Headcount Planning",
            "module": "PABK Manpower",
            "title": "Headcount Planning",
            "label": "Headcount Planning",
            "icon": "users",
            "indicator_color": "blue",
            "is_standard": 1,
            "public": 1,
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
                {"type": "Card Break", "label": "Headcount Planning", "icon": "users"},
                {"type": "Link", "label": "Headcount Plans", "link_type": "DocType", "link_to": "Headcount Plan"},
                {"type": "Link", "label": "Manpower Requisitions", "link_type": "DocType", "link_to": "Manpower Requisition"},
                {"type": "Link", "label": "Employees", "link_type": "DocType", "link_to": "Employee"}
            ]
        })
        workspace.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Created: Headcount Planning workspace")
    
    print("Workspace installed")
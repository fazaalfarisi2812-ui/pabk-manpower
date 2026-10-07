import frappe

def execute():
    # 1. Headcount Plan Item (child table)
    if not frappe.db.exists("DocType", "Headcount Plan Item"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Headcount Plan Item",
            "module": "PABK Manpower",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "job_title", "fieldtype": "Link", "options": "Designation", "label": "Job Title/Designation", "in_list_view": 1},
                {"fieldname": "planned_headcount", "fieldtype": "Int", "label": "Planned", "in_list_view": 1},
                {"fieldname": "actual_headcount", "fieldtype": "Int", "label": "Actual", "in_list_view": 1},
                {"fieldname": "variance", "fieldtype": "Int", "label": "Variance", "in_list_view": 1},
                {"fieldname": "budget", "fieldtype": "Currency", "label": "Budget"},
                {"fieldname": "notes", "fieldtype": "Data", "label": "Notes"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created Headcount Plan Item")
    else:
        print("Headcount Plan Item exists")

    # Add child table to Headcount Plan
    if not frappe.db.exists("Custom Field", "Headcount Plan-items"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Headcount Plan",
            "fieldname": "items",
            "label": "Items",
            "fieldtype": "Table",
            "options": "Headcount Plan Item",
            "insert_after": "department"
        }).insert(ignore_permissions=True)
        print("Added items to Headcount Plan")
    else:
        print("Items field exists on Headcount Plan")

    # 2. Client Placement (SPMK)
    if not frappe.db.exists("DocType", "Client Placement"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Client Placement",
            "module": "PABK Manpower",
            "custom": 1,
            "istable": 0,
            "autoname": "SPMK-.YYYY.-.####",
            "title_field": "client",
            "search_fields": "employee, client, placement_status",
            "fields": [
                {"fieldname": "employee", "fieldtype": "Link", "options": "Employee", "label": "Employee", "reqd": 1, "in_list_view": 1},
                {"fieldname": "employee_name", "fieldtype": "Data", "label": "Employee Name", "fetch_from": "employee.employee_name"},
                {"fieldname": "client", "fieldtype": "Link", "options": "Customer", "label": "Client/Customer", "reqd": 1, "in_list_view": 1},
                {"fieldname": "spmk_number", "fieldtype": "Data", "label": "SPMK Number"},
                {"fieldname": "placement_status", "fieldtype": "Select", "options": "Active\nCompleted\nTerminated", "label": "Status", "default": "Active", "in_list_view": 1},
                {"fieldname": "start_date", "fieldtype": "Date", "label": "Start Date", "reqd": 1},
                {"fieldname": "end_date", "fieldtype": "Date", "label": "End Date"},
                {"fieldname": "job_title", "fieldtype": "Link", "options": "Designation", "label": "Designation/Role"},
                {"fieldname": "location", "fieldtype": "Data", "label": "Placement Location"},
                {"fieldname": "notes", "fieldtype": "Text", "label": "Notes"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created Client Placement")
    else:
        print("Client Placement exists")

    # 3. Timesheet Deployment
    if not frappe.db.exists("DocType", "Timesheet Deployment"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Timesheet Deployment",
            "module": "PABK Manpower",
            "custom": 1,
            "istable": 0,
            "autoname": "TSD-.YYYY.-.####",
            "title_field": "client_placement",
            "search_fields": "employee, client_placement, month",
            "fields": [
                {"fieldname": "employee", "fieldtype": "Link", "options": "Employee", "label": "Employee", "reqd": 1, "in_list_view": 1},
                {"fieldname": "client_placement", "fieldtype": "Link", "options": "Client Placement", "label": "Client Placement (SPMK)", "reqd": 1},
                {"fieldname": "month", "fieldtype": "Select", "options": "January\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember", "label": "Month", "reqd": 1, "in_list_view": 1},
                {"fieldname": "year", "fieldtype": "Data", "label": "Year", "reqd": 1},
                {"fieldname": "total_days", "fieldtype": "Int", "label": "Total Days Present"},
                {"fieldname": "total_overtime", "fieldtype": "Float", "label": "Total Overtime (Hours)"},
                {"fieldname": "status", "fieldtype": "Select", "options": "Draft\nSubmitted\nApproved\nRejected", "label": "Status", "default": "Draft", "in_list_view": 1},
                {"fieldname": "attachment", "fieldtype": "Attach", "label": "Timesheet Attachment"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created Timesheet Deployment")
    else:
        print("Timesheet Deployment exists")

    # 4. Deployment Log
    if not frappe.db.exists("DocType", "Deployment Log"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Deployment Log",
            "module": "PABK Manpower",
            "custom": 1,
            "istable": 0,
            "autoname": "DL-.YYYY.-.####",
            "title_field": "employee",
            "search_fields": "employee, client_placement, log_date",
            "fields": [
                {"fieldname": "employee", "fieldtype": "Link", "options": "Employee", "label": "Employee", "reqd": 1, "in_list_view": 1},
                {"fieldname": "client_placement", "fieldtype": "Link", "options": "Client Placement", "label": "Client Placement (SPMK)", "reqd": 1},
                {"fieldname": "log_date", "fieldtype": "Date", "label": "Log Date", "reqd": 1, "in_list_view": 1},
                {"fieldname": "log_type", "fieldtype": "Select", "options": "Attendance\nOvertime\nLeave\nIncident\nNote", "label": "Log Type", "reqd": 1},
                {"fieldname": "hours", "fieldtype": "Float", "label": "Hours"},
                {"fieldname": "description", "fieldtype": "Text", "label": "Description"},
                {"fieldname": "attachment", "fieldtype": "Attach", "label": "Attachment"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print("Created Deployment Log")
    else:
        print("Deployment Log exists")

    frappe.db.commit()
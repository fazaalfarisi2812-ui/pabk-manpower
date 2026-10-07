
import frappe
def execute():
    try:
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Client Placement",
            "module": "PABK Manpower",
            "custom": 1,
            "istable": 0,
            "naming_rule": "Expression (old style)",
            "autoname": "SPMK-.YYYY.-.####",
            "fields": [
                {"fieldname": "employee", "fieldtype": "Link", "options": "Employee", "label": "Employee", "reqd": 1},
                {"fieldname": "client", "fieldtype": "Link", "options": "Customer", "label": "Client/Customer", "reqd": 1},
                {"fieldname": "job_opening", "fieldtype": "Link", "options": "Job Opening", "label": "Job Opening"},
                {"fieldname": "start_date", "fieldtype": "Date", "label": "Start Date", "reqd": 1},
                {"fieldname": "end_date", "fieldtype": "Date", "label": "End Date"},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": 'Active\nEnded\nTerminated', "default": "Active"},
                {"fieldname": "placement_fee", "fieldtype": "Currency", "label": "Placement/Management Fee"}
            ]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print('Created Client Placement DocType')
    except Exception as e:
        if 'Duplicate' in str(e):
            print('Client Placement DocType already exists')
        else:
            import traceback
            traceback.print_exc()

    try:
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Timesheet Tracking",
            "module": "PABK Manpower",
            "custom": 1,
            "istable": 0,
            "naming_rule": "Expression (old style)",
            "autoname": "TS-.YYYY.-.MM.-.####",
            "fields": [
                {"fieldname": "employee", "fieldtype": "Link", "options": "Employee", "label": "Employee", "reqd": 1},
                {"fieldname": "client", "fieldtype": "Link", "options": "Customer", "label": "Client/Customer"},
                {"fieldname": "month", "fieldtype": "Select", "label": "Month", "options": 'January\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember', "reqd": 1},
                {"fieldname": "year", "fieldtype": "Int", "label": "Year", "reqd": 1},
                {"fieldname": "total_days_worked", "fieldtype": "Float", "label": "Total Days Worked", "reqd": 1},
                {"fieldname": "overtime_hours", "fieldtype": "Float", "label": "Overtime Hours"},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": 'Draft\nSubmitted\nApproved\nInvoiced', "default": "Draft"},
                {"fieldname": "attachment", "fieldtype": "Attach", "label": "Timesheet Document"}
            ]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print('Created Timesheet Tracking DocType')
    except Exception as e:
        if 'Duplicate' in str(e):
            print('Timesheet Tracking DocType already exists')
        else:
            import traceback
            traceback.print_exc()

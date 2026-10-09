frappe.query_reports["Manpower Utilization Trend"] = {
    "filters": [
        {"fieldname": "from_date", "label": "From Date", "fieldtype": "Date", "default": "30_days_ago"},
        {"fieldname": "to_date", "label": "To Date", "fieldtype": "Date", "default": "today"}
    ]
}

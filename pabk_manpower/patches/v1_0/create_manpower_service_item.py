# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe


def execute():
    """Create Manpower Service item for billing"""
    if not frappe.db.exists("Item", "Manpower Service"):
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": "Manpower Service",
            "item_name": "Manpower Service",
            "item_group": "Services",
            "stock_uom": "Hour",
            "is_stock_item": 0,
            "is_service_item": 1,
            "description": "Jasa supply manpower billing per jam",
            "item_defaults": [
                {
                    "company": frappe.defaults.get_user_default("Company"),
                    "default_warehouse": "",
                    "default_price_list": "Standard Selling"
                }
            ]
        })
        item.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger().info("Created Manpower Service item")
    else:
        frappe.logger().info("Manpower Service item already exists")


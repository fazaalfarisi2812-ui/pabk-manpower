from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def get_data():
    return [
        {
            "label": _("Manpower"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Manpower Contract",
                    "description": _("Manage manpower supply contracts with clients"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Manpower Site",
                    "description": _("Client sites where manpower is deployed"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Manpower Requisition",
                    "description": _("Client requests for manpower deployment"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Manpower Shift Assignment",
                    "description": _("Employee shift assignments at client sites"),
                    "onboard": 1,
                },
            ],
        }
    ]


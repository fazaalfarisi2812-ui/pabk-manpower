# Client Placement DocType implementation
# This DocType manages personnel placements at client sites
# Integrated with existing Job Applicant workflow for new hire processing

import frappe

class ClientPlacement:
    def validate(self):
        # Validate placement dates and status transitions
        if self.placement_date and self.end_date:
            if self.end_date < self.placement_date:
                frappe.throw("End date cannot be before start date")
        
        # Auto-calculate status based on dates
        if self.status == "Active" and self.placement_date:
            if self.end_date and self.end_date < frappe.utils.today():
                self.status = "Completed"

    def on_update(self):
        # Update related Manpower Shift Assignments when placement status changes
        if self.status == "Active":
            self._activate_shift_assignments()
        elif self.status == "Completed" or self.status == "Cancelled":
            self._deactivate_shift_assignments()

    def _activate_shift_assignments(self):
        # Link this placement to existing Manpower Shift Assignment records
        pass

    def _deactivate_shift_assignments(self):
        # Mark related shift assignments as inactive
        pass

    def get_placement_summary(self):
        # Return placement details for reporting
        return {
            "placement_name": self.placement_name,
            "client": self.client,
            "site": self.site,
            "employee": self.employee,
            "status": self.status,
            "placement_date": self.placement_date,
            "end_date": self.end_date,
            "billing_rate": self.billing_rate
        }

    def can_be_edited(self):
        # Determine if placement can be modified based on status
        return self.status in ["Draft", "Submitted"]

    def can_be_approved(self):
        # Determine approval eligibility
        return self.status == "Submitted"

    def can_be_completed(self):
        # Determine completion eligibility
        return self.status == "Active"

# Client-side JavaScript for UI enhancements
client_js = """
cur_frm.add_hook('validate', 'client_placement_client.validate');
cur_frm.add_hook('on_update', 'client_placement_client.on_update');

// Auto-calculate end date based on contract term
frappe.ui.form.on('Client Placement', 'contract', function(frm) {
    if (frm.doc.contract) {
        frappe.db.get_value('Manpower Contract', frm.doc.contract, 'end_date', function(contract) {
            if (contract.end_date) {
                // Set end date to contract end date
                frm.set_value('end_date', contract.end_date);
            }
        });
    }
});
"""

# Python-side JavaScript for client-side execution
client_python_js = client_js

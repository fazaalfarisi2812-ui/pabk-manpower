# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

app_name = "pabk_manpower"
app_title = "PABK Manpower"
app_publisher = "PT Puriasri Bhaktikarya"
app_description = "Manpower Management System"
app_email = "quality.management@puriasri.co.id"
app_license = "MIT"

# Document Events
doc_events = {
    "Job Applicant": {
        "after_insert": "pabk_manpower.doctype.job_applicant_enrichment.job_applicant_enrichment.enrich_candidate",
        "on_update": "pabk_manpower.doctype.job_applicant_enrichment.job_applicant_enrichment.enrich_candidate"
    }
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "pabk_manpower.tasks.daily.generate_pending_invoices"
    ]
}

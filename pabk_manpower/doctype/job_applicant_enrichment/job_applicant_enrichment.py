# Copyright (c) 2024, PT Puriasri Bhaktikarya and contributors
# For license information, please see license.txt

import frappe
import requests
import re
from urllib.parse import urlparse
from frappe.utils import now_datetime


def enrich_candidate_from_linkedin(linkedin_url):
    """
    Fetch public LinkedIn profile data.
    Note: LinkedIn blocks automated scraping. This is a placeholder for:
    - LinkedIn API (requires partnership)
    - Manual entry + webhook from browser extension
    - Third-party enrichment services (free tiers: Proxycurl, RapidAPI)
    """
    # Placeholder - in production, use:
    # 1. LinkedIn API (Partner)
    # 2. Proxycurl API (free tier: 10 req/month)
    # 3. RapidAPI LinkedIn scrapers
    # 4. Browser extension that posts to webhook
    
    skills = []
    experience = []
    
    # Extract username from URL for reference
    parsed = urlparse(linkedin_url)
    username = parsed.path.strip("/").split("/")[-1]
    
    return {
        "skills": skills,
        "experience": experience,
        "source": "linkedin",
        "profile_id": username
    }


def enrich_candidate_from_github(github_url):
    """
    Fetch public GitHub profile data via GitHub API (no auth needed for public data).
    Rate limit: 60 req/hour unauthenticated, 5000/hour with token.
    """
    try:
        # Extract username from URL
        parsed = urlparse(github_url)
        username = parsed.path.strip("/").split("/")[-1]
        
        # GitHub API - public user data
        api_url = f"https://api.github.com/users/{username}"
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        # Add token if available (set in site_config.json or env)
        github_token = frappe.conf.get("github_token") or frappe.get_system_settings("github_token")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Get repos for skills inference
            repos_url = f"https://api.github.com/users/{username}/repos"
            repos_response = requests.get(repos_url, headers=headers, timeout=10)
            
            languages = set()
            if repos_response.status_code == 200:
                for repo in repos_response.json()[:20]:  # Limit to 20 repos
                    if repo.get("language"):
                        languages.add(repo["language"])
            
            skills = list(languages)
            experience = [{
                "company": data.get("company") or "Open Source",
                "role": "Developer",
                "description": data.get("bio") or "",
                "url": data.get("html_url")
            }]
            
            return {
                "skills": skills,
                "experience": experience,
                "source": "github",
                "profile_id": username,
                "public_repos": data.get("public_repos", 0),
                "followers": data.get("followers", 0)
            }
        else:
            return {"error": f"GitHub API error: {response.status_code}", "source": "github"}
            
    except Exception as e:
        return {"error": str(e), "source": "github"}


def enrich_candidate(doc, method):
    """
    Hook: Triggered on Job Applicant insert/update.
    Enriches candidate profile from LinkedIn/GitHub URLs.
    """
    # Only enrich if URLs provided and not already enriched
    if not (doc.linkedin_url or doc.github_url):
        return
    
    # Check if URLs have changed since last enrichment
    last_github = getattr(doc, "_last_enriched_github", None)
    last_linkedin = getattr(doc, "_last_enriched_linkedin", None)
    
    if doc.enrichment_status == "Completed" and doc.github_url == last_github and doc.linkedin_url == last_linkedin:
        # Already enriched with same URLs, skip unless forced
        return
    
    # Update status
    doc.db_set("enrichment_status", "In Progress", update_modified=False)
    
    all_skills = []
    all_experience = []
    errors = []
    
    # Enrich from LinkedIn
    if doc.linkedin_url:
        try:
            linkedin_data = enrich_candidate_from_linkedin(doc.linkedin_url)
            if "error" not in linkedin_data:
                all_skills.extend(linkedin_data.get("skills", []))
                all_experience.extend(linkedin_data.get("experience", []))
            else:
                errors.append(f"LinkedIn: {linkedin_data['error']}")
        except Exception as e:
            errors.append(f"LinkedIn: {str(e)}")
    
    # Enrich from GitHub
    if doc.github_url:
        try:
            github_data = enrich_candidate_from_github(doc.github_url)
            if "error" not in github_data:
                all_skills.extend(github_data.get("skills", []))
                all_experience.extend(github_data.get("experience", []))
            else:
                errors.append(f"GitHub: {github_data['error']}")
        except Exception as e:
            errors.append(f"GitHub: {str(e)}")
    
    # Deduplicate skills
    unique_skills = list(dict.fromkeys(all_skills))
    
    # Update document
    doc.db_set("enriched_skills", ", ".join(unique_skills) if unique_skills else "", update_modified=False)
    doc.db_set("enriched_experience", frappe.as_json(all_experience, indent=2) if all_experience else "", update_modified=False)
    doc.db_set("enrichment_status", "Failed" if errors and not unique_skills else "Completed", update_modified=False)
    doc.db_set("enrichment_date", now_datetime(), update_modified=False)
    
    if errors:
        frappe.log_error(f"Candidate enrichment errors for {doc.name}: {errors}", "Job Applicant Enrichment")


@frappe.whitelist()
def manual_enrich(job_applicant_name):
    """Manual enrichment trigger from client"""
    doc = frappe.get_doc("Job Applicant", job_applicant_name)
    enrich_candidate(doc, "manual")
    doc.reload()
    return {"status": doc.enrichment_status, "skills": doc.enriched_skills, "experience": doc.enriched_experience}


@frappe.whitelist()
def get_github_token():
    """Check if GitHub token is configured"""
    token = frappe.conf.get("github_token") or frappe.get_system_settings("github_token")
    return {"configured": bool(token)}


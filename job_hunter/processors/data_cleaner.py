import os
import json

def clean_raw_jobs(raw_jobs):
    """
    Basic cleaning: remove empty titles/links, normalize strings.
    Strictly filter to only target jobs specified in keywords.json.
    """
    keywords_path = os.path.join(os.path.dirname(__file__), "..", "config", "keywords.json")
    with open(keywords_path, 'r') as f:
        data = json.load(f)
        target_titles = [title.lower() for title in data.get("titles", [])]
        
    cleaned = []
    seen_links = set()
    
    for job in raw_jobs:
        if not job.get('title') or not job.get('link'):
            continue
            
        title_lower = job['title'].lower()
        # Strictly target only this kind of jobs
        if not any(target in title_lower for target in target_titles):
            continue
            
        link = job['link'].strip()
        if link in seen_links:
            continue
            
        seen_links.add(link)
        
        cleaned.append({
            "title": job['title'].strip(),
            "company": job.get('company', 'Unknown').strip(),
            "location": job.get('location', '').strip(),
            "link": link,
            "description": job.get('description', '').strip()
        })
        
    return cleaned

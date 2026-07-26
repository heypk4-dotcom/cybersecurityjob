def clean_raw_jobs(raw_jobs):
    """
    Basic cleaning: remove empty titles/links, normalize strings.
    """
    cleaned = []
    seen_links = set()
    
    for job in raw_jobs:
        if not job.get('title') or not job.get('link'):
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

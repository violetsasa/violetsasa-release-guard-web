import os
import hashlib
import json
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- CONFIGURATION ---
URLS_TO_TRACK = {
    "Apple News": "https://developer.apple.com/news/",
    "Android Blog": "https://android-developers.googleblog.com/",
    "Steamworks": "https://steamcommunity.com/groups/steamworks/announcements"
}

CACHE_FILE = "automation/cache.json"

# Secrets (from GitHub Actions)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
EMAIL_FROM = SMTP_USER
EMAIL_TO = os.environ.get("EMAIL_TO")

def get_page_hash(url):
    """Fetches page content and returns a hash of the text."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Simple extraction: visible text. Can be refined per site.
        text = soup.get_text()
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def send_email(updates):
    if not SMTP_USER or not SMTP_PASS or not EMAIL_TO:
        print("Skipping email: Missing environment variables (SMTP_USER, SMTP_PASS, EMAIL_TO).")
        return

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = f"Release Guard Briefing: {datetime.now().strftime('%Y-%m-%d')}"

    body = "<h2>Release Guard - Daily Monitoring</h2>\n"
    if updates:
        body += "<p>The following pages have potential updates:</p><ul>"
        for site, url in updates:
            body += f"<li><strong>{site}</strong>: <a href='{url}'>{url}</a></li>"
        body += "</ul>"
    else:
        body += "<p>No changes detected in the tracked pages.</p>"
    
    body += "<br><p><em>Powered by Release Guard Automation</em></p>"

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    print("Starting Daily Brief...")
    cache = load_cache()
    updates = []
    
    new_cache = cache.copy()

    for name, url in URLS_TO_TRACK.items():
        print(f"Checking {name}...")
        current_hash = get_page_hash(url)
        
        if current_hash:
            last_hash = cache.get(url)
            if last_hash != current_hash:
                print(f"-> CHANGE DETECTED: {name}")
                if last_hash is not None: # Don't alert on first run (initial seed)
                    updates.append((name, url))
            else:
                print(f"-> No change: {name}")
            
            new_cache[url] = current_hash

    save_cache(new_cache)
    
    if updates:
        print(f"Found {len(updates)} updates. Sending notification...")
        send_email(updates)
    else:
        print("No meaningful updates found.")

if __name__ == "__main__":
    main()

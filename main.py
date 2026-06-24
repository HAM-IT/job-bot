import os
import requests
import json
from jobspy import scrape_jobs

# L'URL segreto preso da GitHub Secrets
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def main():
    print("🔍 Avvio ricerca lavori...")
    
   # 1. Scraper (Filtri aggiornati per Operations/PMO)
    jobs = scrape_jobs(
        site_name=["indeed", "google", "linkedin"], # <-- Aggiunto qui
        search_term="PMO OR Operations OR Supply Chain",
        location="Morocco",
        results_wanted=10, 
        hours_old=72,
        country_indeed="morocco"
    )
    
    if jobs.empty:
        print("Nessun lavoro trovato oggi.")
        return

    # 2. Formatta i dati per Google (seleziona solo le colonne che ci servono)
    jobs_clean = jobs[['title', 'company', 'location', 'job_url', 'description']].fillna("").to_dict(orient="records")
    
    # 3. Spedisci al Webhook di Google
    print(f"🚀 Spedizione di {len(jobs_clean)} lavori a Google Apps Script...")
    headers = {'Content-Type': 'application/json'}
    response = requests.post(WEBHOOK_URL, data=json.dumps(jobs_clean), headers=headers)
    
    if response.status_code == 200:
        print("✅ Dati ricevuti da Google con successo!")
    else:
        print(f"❌ Errore nella spedizione: {response.text}")

if __name__ == "__main__":
    main()

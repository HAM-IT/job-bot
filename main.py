import os
import requests
import json
from jobspy import scrape_jobs

# L'URL segreto preso da GitHub Secrets
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def main():
    print("🔍 Avvio ricerca lavori...")
    
    # 1. Scraper (puoi personalizzare i parametri)
    jobs = scrape_jobs(
        site_name=["indeed", "google"],
        search_term="PMO Analyst",
        location="Milan, Italy",
        results_wanted=5, # Tienilo basso all'inizio per non sovraccaricare Google Apps Script
        hours_old=24,
        country_indeed="Italy"
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

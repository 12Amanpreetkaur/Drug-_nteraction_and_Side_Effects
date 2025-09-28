<<<<<<< HEAD
# Drug Interaction & Side-Effect Alert App — Prototype

This is a self-contained prototype you can run locally. It includes:
- A Flask backend (`backend/`) with a small SQLite database and endpoints:
    - `GET /api/drugs` - list drugs
    - `POST /api/add_drug` - add single drug
    - `POST /api/check_interactions` - check pairwise interactions for a list of meds
    - `POST /api/import_csv` - upload CSV to bulk-import interactions (columns: drug_a,drug_b,severity,note)
    - `POST /api/rxnorm_lookup` - local lookup by name or rxnorm_id (prototype — no external calls)
    - `POST /api/ai_query` - placeholder for LLM integration
- A minimal web UI (`backend/templates/index.html`) served by Flask.
- Sample CSV (`backend/data/sample_interactions.csv`).
- Android WebView wrapper skeleton (`android/`).

## How to run (backend)
1. Open a terminal.
2. Navigate to `backend/`:
    ```bash
    cd /path/to/drug-safety-app/backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python db_init.py
    python app.py
    ```
3. Visit `http://127.0.0.1:5000/` in your browser. If running on a laptop and testing with a phone WebView, use your laptop's local IP (e.g., `http://192.168.1.10:5000/`) and ensure both devices are on the same network.

## CSV format for import
The CSV must have headers:
```
drug_a,drug_b,severity,note
```
Example row:
```
Aspirin,Warfarin,high,Increased bleeding risk
```

## RxNorm integration (production notes)
- This prototype provides `rxnorm_lookup` that searches the local DB.
- For real RxNorm lookup, call the NIH RxNorm REST API from the backend, map RxCUI to drug names, and store `rxnorm_id` in `drugs` table.
- Example external API (for production): https://rxnav.nlm.nih.gov/RxNormAPIs.html

## Android wrapper
- Open Android Studio, create an Empty Activity project, replace `MainActivity.kt` and `AndroidManifest.xml` with the ones provided.
- Change `START_URL` to your server's address.

## Security & Compliance (important)
- This is a prototype. Do not use in production without:
  - Proper authentication & authorization
  - HTTPS (TLS)
  - Data encryption at rest & in transit
  - Pharmacist validation of the drug interaction data
  - Legal review for HIPAA/GDPR compliance if handling PHI

## Next steps I can do for you
- Add an RxNorm import script (pulling RxCUI data) — requires web access/API key.
- Add user accounts and encrypted local storage.
- Implement LLM forwarding with safe prompt templates & pharmacist-review workflow.
=======
# Drug-_nteraction_and_Side_Effects
>>>>>>> c69c4fcbc889f2edc767e8d86ad747922f369304

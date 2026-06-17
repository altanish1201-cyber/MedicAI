# 🏥 MedicAI: Multi-Agent Clinical Translation Pipeline

**Bridging India's Health Literacy Gap Through Intelligent Multi-Agent Systems.**

Built by **Team BioBackers** (SIT Pune - Division A-2) as a clinical translation and triage system. 

---

## 🚨 The Silent Crisis in Healthcare

* **Low Health Literacy:** Over 60-90% of patients in rural areas struggle to comprehend complex diagnostic reports (WHO, 2025).
* **Clinical Jargon:** Terminology like *myocardial infarction*, *ST-elevation*, or *tachycardia* creates anxiety and delays critical interventions.
* **Localization Gap:** Most clinical documentation is generated in English, leaving non-English speakers dependent on manual, error-prone translations.

**MedicAI** resolves this by translating complex medical report texts and image scans into easy-to-read, localized insights in under 30 seconds.

---

## 🧠 The 5-Agent Architecture

MedicAI implements a robust multi-agent pipeline using **Groq (Llama-3.1)** and **Tesseract OCR** for step-by-step audit, verification, and formatting:

```
[ Input Report ]
       │
       ▼
 1. 👁️ [Vision Agent] ──────► Uses OCR to extract text from scan images (Tesseract)
       │
       ▼
 2. 🛡️ [Triage Agent] ──────► Flags emergency indicators & determines structured risk levels (JSON)
       │
       ▼
 3. 🧠 [Simplifier Agent] ──► Explains complex jargon at a 5th-grade reading level (Layman English)
       │
       ▼
 4. 🕵️ [Auditor Agent] ─────► Clinically reviews the summary to prevent hallucinations/omissions
       │
       ▼
 5. 🌐 [Translator Agent] ──► Localizes verified details into Hindi or Marathi (Devanagari script)
       │
       ▼
 6. 🏡 [Home Care Agent] ───► Generates safe, localized home care precautions
```

---

## ✨ Features

* **Visual Risk Dashboard:** Triage assessments are dynamically parsed from structured JSON, rendering color-coded risk blocks based on severity (High, Moderate, Low).
* **Self-Correcting Audit Flow:** The Clinical Auditor Agent actively checks the Simplifier Agent's output against the original report to ensure clinical accuracy.
* **OCR Graceful Failover:** Detects if the Tesseract binary is missing on the local machine and presents structured setup guides instead of crash traces.
* **Theme-Adaptive Glassmorphic UI:** A clean, modern Streamlit layout supporting light and dark modes.
* **Secure Token Handling:** Environment configuration via `.env` files or sidebar key input overrides to prevent key leaks.

---

## 🚀 Running Locally

### 1. Prerequisites
Ensure you have **Python 3.9+** and the **Tesseract OCR engine** installed:
* **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
* **MacOS:** `brew install tesseract`
* **Windows:** Download the installer from the [UB Mannheim build repository](https://github.com/UB-Mannheim/tesseract/wiki) and add it to your system environment variables.

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/altanish1201-cyber/MedicAI.git
cd MedicAI
```

Create a virtual environment and install packages:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt python-dotenv
```

### 3. API Credentials
Copy the template and add your Groq key:
```bash
cp .env.template .env
```
Open `.env` and configure:
```text
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Boot the Application
Run the Streamlit server:
```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack
* **Frontend/Dashboard:** Streamlit (Python)
* **LLM Engine:** Groq API (Llama-3.1-8b-instant)
* **OCR Extraction:** Pytesseract (Tesseract OCR Engine)
* **Environment:** Dotenv (Python)

---

## 👥 Project Team
**Team BioBackers** (SIT Pune | Division A-2)
* Aditi Pandey
* Niharika Bhalerao
* Anish Kumar Sahu
* Aman Choudhary

*Disclaimer: This project is a prototype for educational and informational purposes only. It is not intended to replace professional medical advice.*

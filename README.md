# 🏥 MedicAI: Agentic Medical Translator

**Bridging India's Health Literacy Gap Through Intelligent Multi-Agent Translation.**

Built by **Team BioBackers** (SIT Pune - Division A-2) for **STARTUPCON 5.0**.

---

## 🚨 The Silent Crisis

-  **60-90% of Indians** have low health literacy (WHO, 2025).
-  **Only 38%** of rural patients fully understand their diagnosis.
-  **70% of patients** misunderstand common medical terms (e.g., myocardial infarction, dyspnea).

 Medical jargon leads to patient confusion, non-compliance with medication, and dangerous delayed treatments.  MedicAI solves this by transforming complex medical findings into layman-friendly, localized reports in under 30 seconds.
## 🧠 The 5-Agent Architecture

This is not a simple translation wrapper. MedicAI utilizes a specialized Multi-Agent Intelligence pipeline powered by Groq (Llama-3.1) and Tesseract OCR:

1.  **👁️ Input Parser Agent:** Extracts structured text from medical PDFs and physical scans.
2.  **🛡️ Triage & Risk Agent:** Autonomously flags critical conditions (e.g., ST-elevation) for urgent care.
3.  **🧠 Simplifier Agent:** Converts heavy medical jargon into plain English at a 5th-grade reading level.
4. **🕵️ Reviewer Agent:** Acts as a strict clinical auditor to prevent AI hallucinations and ensure medical accuracy.
5.  **🌐 Translation Agent:** Localizes the simplified English directly into native Hindi and Marathi (Devanagari script) to serve 60% of rural India.
6.  **🏡 Home Care Agent:** Generates safe, actionable next steps and at-home precautions.

## 🚀 How to Run Locally

### Prerequisites

You need Python 3.9+ and the Tesseract OCR engine installed on your system.

- **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
- **Mac (Homebrew):** `brew install tesseract`

### Installation

1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/medic-ai.git](https://github.com/YOUR_USERNAME/medic-ai.git)
   cd medic-ai
   ```

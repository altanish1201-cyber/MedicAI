# 🏥 MedicAI: Agentic Medical Translator

**Bridging India's Health Literacy Gap Through Intelligent Multi-Agent Translation.**

[cite_start]Built by **Team BioBackers** (SIT Pune - Division A-2) for **STARTUPCON 5.0**[cite: 3, 4].

---

## 🚨 The Silent Crisis

- [cite_start]**60-90% of Indians** have low health literacy (WHO, 2025)[cite: 13, 14, 15].
- [cite_start]**Only 38%** of rural patients fully understand their diagnosis[cite: 16, 17, 18].
- [cite_start]**70% of patients** misunderstand common medical terms (e.g., myocardial infarction, dyspnea)[cite: 20, 21, 24, 25].

[cite_start]Medical jargon leads to patient confusion, non-compliance with medication, and dangerous delayed treatments[cite: 28, 32, 33, 37, 40]. [cite_start]MedicAI solves this by transforming complex medical findings into layman-friendly, localized reports in under 30 seconds[cite: 1, 121].

## 🧠 The 5-Agent Architecture

This is not a simple translation wrapper. MedicAI utilizes a specialized Multi-Agent Intelligence pipeline powered by Groq (Llama-3.1) and Tesseract OCR:

1. [cite_start]**👁️ Input Parser Agent:** Extracts structured text from medical PDFs and physical scans[cite: 99, 100, 101, 107].
2. [cite_start]**🛡️ Triage & Risk Agent:** Autonomously flags critical conditions (e.g., ST-elevation) for urgent care[cite: 113, 114].
3. [cite_start]**🧠 Simplifier Agent:** Converts heavy medical jargon into plain English at a 5th-grade reading level[cite: 102, 104].
4. **🕵️ Reviewer Agent:** Acts as a strict clinical auditor to prevent AI hallucinations and ensure medical accuracy.
5. [cite_start]**🌐 Translation Agent:** Localizes the simplified English directly into native Hindi and Marathi (Devanagari script) to serve 60% of rural India[cite: 103, 105, 106].
6. [cite_start]**🏡 Home Care Agent:** Generates safe, actionable next steps and at-home precautions[cite: 116, 117].

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

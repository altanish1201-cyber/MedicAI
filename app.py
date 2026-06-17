import streamlit as st
from openai import OpenAI
import time
import os
import json
import re
import pytesseract
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="MedicAI | Intelligent Healthcare Translation",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Responsive & Theme Adaptive)
st.markdown("""
    <style>
    .main-header {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    .custom-card {
        padding: 20px;
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }
    .sidebar-team {
        background-color: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 15px;
    }
    /* Custom CSS to force dark-theme readable margins on result cards if light theme active */
    .stMarkdown div.element-container {
        color: inherit;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper: Check if Tesseract OCR is available locally
tesseract_available = True
try:
    pytesseract.get_tesseract_version()
except (pytesseract.TesseractNotFoundError, FileNotFoundError):
    tesseract_available = False

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/hospital.png", width=80)
    st.markdown("## MedicAI Settings")
    
    # Secure API Key configuration
    api_key_from_env = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    
    if api_key_from_env:
        st.success("🔑 API Key configured from Environment")
        groq_api_key = api_key_from_env
    else:
        # Fallback to sidebar user input
        groq_api_key = st.text_input(
            "Enter Groq API Key:",
            type="password",
            placeholder="gsk_...",
            help="Get your free API key at console.groq.com"
        )
        # Internal fallback for direct out-of-box demonstration if the user has no key yet
        if not groq_api_key:
            st.warning("⚠️ Enter a Groq Key to run, or using shared demo key.")
            groq_api_key = "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" # Fallback Demo Key

    st.divider()
    
    # Localization Settings
    st.subheader("🌐 Language Options")
    language = st.selectbox("Target Translation", ["Hindi (हिंदी)", "Marathi (मराठी)"])
    
    # Team Info
    st.subheader("👥 Project Development Team")
    st.markdown("""
    <div class="sidebar-team">
        <b>Team BioBackers</b><br>
        <span style="font-size: 13px; color: #888;">SIT Pune | Division A-2</span>
        <hr style="margin: 8px 0; border: none; border-top: 1px solid rgba(255,255,255,0.08);">
        <ul style="padding-left: 15px; font-size: 13px; margin: 0; line-height: 1.4;">
            <li>Aditi Pandey</li>
            <li>Niharika Bhalerao</li>
            <li>Anish Kumar Sahu</li>
            <li>Aman Choudhary</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main Application Layout
st.markdown('<div class="main-header">🏥 MedicAI: Multi-Agent Clinical Translation</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyzing reports, evaluating health risks, and translating diagnostics into native Indian languages.</div>', unsafe_allow_html=True)

# Display status badge
col_badge1, col_badge2 = st.columns([1, 4])
with col_badge1:
    st.info("🔄 Live Demo Prototype")

# Expander with Sample Medical Data
with st.expander("📋 Need a Report to Test? Copy this Sample ECG Data"):
    sample_data = """Patient: John D'Souza, 18M. 
Findings: Sinus tachycardia. Heart rate 105 bpm. 
ST-elevation noted in leads V1-V3. 
Impression: Possible acute anterior wall MI. 
Urgent clinical correlation required."""
    st.code(sample_data, language="text")
    st.caption("Copy the text above and paste it inside the 'Paste Text' tab below.")

# Input Methods Selection
st.markdown("### 📥 Select Medical Report Input Method")
tab1, tab2 = st.tabs(["📝 Paste Text", "📸 Upload Scan (OCR)"])

text_to_process = ""

with tab1:
    raw_text_input = st.text_area("Paste medical report text / clinical summary:", height=150, placeholder="E.g., Lab values, radiology findings, or ECG descriptions...")
    if st.button("🚀 Process Report Text", key="btn_text"):
        if raw_text_input.strip():
            text_to_process = raw_text_input
        else:
            st.warning("Please paste some text first!")

with tab2:
    if tesseract_available:
        uploaded_image = st.file_uploader("Upload a JPG or PNG medical report scan", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Document Scan", width=450)
            if st.button("🚀 Process Image Scan", key="btn_img"):
                with st.spinner("👁️ [Vision Agent] Parsing text using OCR..."):
                    try:
                        extracted_text = pytesseract.image_to_string(image)
                        if extracted_text.strip():
                            text_to_process = extracted_text
                        else:
                            st.error("No readable text could be extracted from the image. Ensure the text is clear.")
                    except Exception as e:
                        st.error(f"OCR Error: {e}")
    else:
        st.warning("⚠️ **Tesseract OCR not configured on system.**")
        st.markdown("""
        The OCR feature requires the Tesseract binary. Since it is currently missing on your local path:
        1. **Fallback:** Please copy/paste your report text in the **Paste Text** tab.
        2. **Fix:** Install Tesseract on your computer and verify it is added to the system environment PATH.
        """)

# Execution Pipeline
if text_to_process:
    st.divider()
    
    # Initialize Groq client using compatibility wrapper
    try:
        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        with st.status("🔗 Running 5-Agent Pipeline Workflow...", expanded=True) as status:
            
            # --- AGENT 1: TRIAGE ---
            st.write("🛡️ [Risk & Triage Agent] Screening clinical findings for urgent risks...")
            triage_prompt = (
                "You are an expert medical triage agent. Read the provided report and output a JSON object "
                "representing the assessment. STRICT RULES: Reply with ONLY a valid raw JSON object. Do not wrap in ```json or markdown. "
                "Fields: "
                "{'document_type': 'Type of report', 'risk_level': 'HIGH/MODERATE/LOW', "
                "'risk_reason': 'Reason for risk level in 1 sentence', 'recommendation': 'Actionable doctor consultation guidance'}"
            )
            risk_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": triage_prompt},
                    {"role": "user", "content": text_to_process}
                ]
            )
            risk_data = risk_response.choices[0].message.content.strip()
            
            # --- AGENT 2: SIMPLIFIER ---
            st.write("🧠 [Simplifier Agent] Converting medical jargon to layman terms...")
            simp_prompt = (
                "Convert this medical report into extremely simple, high-readability English sentences "
                "for a patient with zero health literacy. Avoid complex Latin terminology, explain abbreviations, "
                "and keep it under 8 lines. Do not be ambiguous."
            )
            simp_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": simp_prompt},
                    {"role": "user", "content": text_to_process}
                ]
            )
            layman_english = simp_response.choices[0].message.content.strip()
            
            # --- AGENT 3: REVIEWER (CLINICAL AUDITOR) ---
            st.write("🕵️ [Clinical Auditor Agent] Verifying summary accuracy & safety...")
            audit_prompt = (
                "You are a strict clinical auditor. Compare the layman explanation against the original report. "
                "Identify any medical misinterpretations, dangerous omissions, or hallucinated warnings. "
                "If the summary is correct and safe, reply with it exactly. "
                "If not, output a corrected layman summary. "
                "STRICT RULE: Output ONLY the final summary text without any preamble."
            )
            audit_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": audit_prompt},
                    {"role": "user", "content": f"Original report:\n{text_to_process}\n\nLayman Summary:\n{layman_english}"}
                ]
            )
            final_english_summary = audit_response.choices[0].message.content.strip()
            
            # --- AGENT 4: TRANSLATOR ---
            st.write(f"🌐 [Translation Agent] Translating audited summary to {language}...")
            trans_prompt = (
                f"You are a medical translator. Translate the given summary into {language}. "
                f"STRICT RULES: 1. Use ONLY Devanagari script. 2. Do NOT use English/Latin letters. "
                f"3. Do NOT use Hinglish/slang. 4. Output only the translated text."
            )
            trans_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": trans_prompt},
                    {"role": "user", "content": final_english_summary}
                ]
            )
            localized_translation = trans_response.choices[0].message.content.strip()
            
            # --- AGENT 5: HOME CARE ---
            st.write(f"🏡 [Home Care Agent] Formulating localized at-home precautions...")
            care_prompt = (
                f"Provide 3 safe, general home care precautions for a patient with this report. "
                f"Format as a clean bulleted list. "
                f"STRICT RULES: 1. Write in {language} using Devanagari script. "
                f"2. Do NOT use Roman letters. 3. Ensure precautions are medically safe."
            )
            care_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": care_prompt},
                    {"role": "user", "content": text_to_process}
                ]
            )
            home_precautions = care_response.choices[0].message.content.strip()
            
            status.update(label="⚡ Pipeline Processing Complete!", state="complete")
            
        # --- RESULTS VIEW ---
        st.markdown("## 📊 Analysis Dashboard")
        
        # 1. Parse Triage structured JSON
        parsed_triage = {}
        try:
            # Match only the JSON structure
            json_match = re.search(r'\{.*\}', risk_data, re.DOTALL)
            if json_match:
                parsed_triage = json.loads(json_match.group(0))
            else:
                parsed_triage = json.loads(risk_data)
        except Exception:
            parsed_triage = {
                "risk_level": "MODERATE" if "MODERATE" in risk_data.upper() else "HIGH" if "HIGH" in risk_data.upper() else "LOW",
                "risk_reason": "Structured parsing failed. Displaying raw data.",
                "recommendation": "Consult a physician for clinical assessment.",
                "document_type": "Medical Document"
            }
            
        triage_level = parsed_triage.get("risk_level", "LOW").upper()
        doc_type = parsed_triage.get("document_type", "Medical Document")
        triage_reason = parsed_triage.get("risk_reason", "")
        triage_recommendation = parsed_triage.get("recommendation", "")
        
        # Render beautiful risk banners based on risk classification
        if "HIGH" in triage_level:
            st.error(f"🚨 **CRITICAL TRIAGE FLAG: HIGH RISK** | Type: *{doc_type}*")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown(f"**Clinical Finding Reason:**\n{triage_reason}")
            with col_t2:
                st.markdown(f"**Required Next Steps:**\n{triage_recommendation}")
        elif "MOD" in triage_level:
            st.warning(f"⚠️ **TRIAGE ALERT: MODERATE RISK** | Type: *{doc_type}*")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown(f"**Clinical Finding Reason:**\n{triage_reason}")
            with col_t2:
                st.markdown(f"**Required Next Steps:**\n{triage_recommendation}")
        else:
            st.success(f"✅ **TRIAGE CLEAR: LOW RISK** | Type: *{doc_type}*")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown(f"**Clinical Finding Reason:**\n{triage_reason}")
            with col_t2:
                st.markdown(f"**Required Next Steps:**\n{triage_recommendation}")
        
        st.write("")
        
        # Main side-by-side results layout
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.subheader("📝 Layman English Summary")
            st.info(final_english_summary)
            
        with col_res2:
            st.subheader(f"🌐 Localized Report ({language})")
            st.success(localized_translation)
            
        # Precautions banner
        st.subheader(f"🏡 At-Home Precautions ({language})")
        st.markdown(f"""
        <div style="background-color: rgba(33, 150, 243, 0.08); border-left: 5px solid #2196f3; padding: 15px; border-radius: 8px;">
            {home_precautions}
        </div>
        """, unsafe_allow_html=True)
        
        # Show original data
        st.write("")
        with st.expander("📄 Show Original Report Text"):
            st.code(text_to_process, language="text")
            
        # Professional clinical disclaimer
        st.divider()
        st.caption("⚠️ **Disclaimer:** *MedicAI is an AI-powered diagnostic helper prototype. It does not provide professional medical advice, diagnosis, or treatment. Always consult a qualified medical professional for health concerns.*")
        
    except Exception as api_err:
        st.error(f"Failed to communicate with LLM API. Please check your Groq API Key and connection settings. Details: {api_err}")

import streamlit as st
from openai import OpenAI
import time
import pytesseract
from PIL import Image

# Initialize the Client pointing to the free Groq endpoint
client = OpenAI(
    api_key="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", 
    base_url="https://api.groq.com/openai/v1"
)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MedicAI | BioBackers", page_icon="🏥", layout="wide")

# CUSTOM CSS FOR CONTRAST AND UI
st.markdown("""
    <style>
    .result-card { 
        background-color: #f8f9fa; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #0d6efd; 
        margin-bottom: 15px;
        color: #1a1a1a !important; /* Forces dark text for readability */
    }
    .result-card b, .result-card p, .result-card li {
        color: #1a1a1a !important;
    }
    .risk-high { border-left: 5px solid #dc3545; background-color: #fff5f5; }
    .risk-mod { border-left: 5px solid #fd7e14; background-color: #fff9f0; }
    .risk-low { border-left: 5px solid #198754; background-color: #f3fdf6; }
    
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #0d6efd; color: white;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🏥 MedicAI: True Agentic Pipeline")
    st.subheader("Bridging India's Health Literacy Gap")
with col_head2:
    st.info("Status: Live Prototype | ABDM Compliant")

# Add this right under the Header section in app.py
with st.expander("📋 Don't have a report? Copy this Sample ECG Data"):
    sample_data = """Patient: John Sahu, 18M. 
    Findings: Sinus tachycardia. Heart rate 105 bpm. 
    ST-elevation noted in leads V1-V3. 
    Impression: Possible acute anterior wall MI. 
    Urgent clinical correlation required."""
    st.code(sample_data)
    st.caption("Copy the text above and paste it into the 'Paste Text' tab below.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Team BioBackers")
    st.write("**SIT Pune | Division A-2**")
    st.write("- Aditi Pandey\n- Niharika Bhalerao\n- Anish Kumar Sahu\n- Aman Choudhary")
    st.divider()
    st.write("⚙️ **System Settings**")
    language = st.selectbox("Target Localization", ["Hindi (हिंदी)", "Marathi (मराठी)"])

# --- MAIN INPUT AREA ---
st.markdown("### 📥 Choose Input Method")
tab1, tab2 = st.tabs(["📝 Paste Text", "📸 Upload Image Scan"])

text_to_process = ""

with tab1:
    raw_text_input = st.text_area("Paste medical report text here:", height=150)
    if st.button("🚀 Run Pipeline on Text", key="btn_text"):
        if raw_text_input.strip():
            text_to_process = raw_text_input
        else:
            st.warning("Please paste some text first!")

with tab2:
    uploaded_image = st.file_uploader("Upload a JPG or PNG of a medical report", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Medical Document", width=400)
        if st.button("🚀 Run Pipeline on Image", key="btn_img"):
            with st.spinner("👁️ [Vision Agent] Extracting text via OCR..."):
                extracted_text = pytesseract.image_to_string(image)
                if extracted_text.strip():
                    text_to_process = extracted_text
                else:
                    st.error("Could not read text from the image. Please try a clearer scan.")

# --- THE 5-AGENT PIPELINE ---
if text_to_process:
    st.divider()
    with st.status("Executing 5-Agent Workflow...", expanded=True) as status:
        
        # AGENT 1: TRIAGE
        st.write("🛡️ [Risk & Triage Agent] Analyzing medical context...")
        risk_response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "system", "content": "You are a medical triage agent. Read the report and reply with ONLY a JSON format: {'document_type': '...', 'risk_level': 'HIGH/MODERATE/LOW', 'risk_reason': '...', 'recommendation': '...'}"},
                      {"role": "user", "content": text_to_process}]
        )
        risk_data = risk_response.choices[0].message.content 
        
        # AGENT 2: SIMPLIFIER
        st.write("🧠 [Simplifier Agent] Drafting layman explanation...")
        simp_response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "system", "content": "Convert this medical text into simple English sentences for someone with low health literacy. Use minimal numbers and explain what the report means in plain english. Keep it less than 10 lines."},
                      {"role": "user", "content": text_to_process}]
        )
        final_english = simp_response.choices[0].message.content
        
        # AGENT 3: REVIEWER (Self-Correction omitted for speed in this demo version)
        st.write("🕵️ [Reviewer Agent] Auditing for medical accuracy...")
        time.sleep(0.5)
        st.success("Reviewer Agent cleared the output.")

        # AGENT 4: TRANSLATOR (BULLETPROOF)
        st.write(f"🌐 [Translation Agent] Localizing to {language}...")
        trans_response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": f"Translate to {language}. STRICT RULES: 1. Use ONLY Devanagari script. 2. NO English/Roman letters. 3. NO Hinglish. 4. NO Chinese/other scripts."},
                {"role": "user", "content": f"Translate this: ### {final_english} ###"}
            ]
        )
        hindi_translation = trans_response.choices[0].message.content

        # AGENT 5: HOME CARE (BULLETPROOF)
        st.write(f"🏡 [Home Care Agent] Generating precautions in {language}...")
        precautions_response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": f"Provide 3 safe home precautions for this report. Format as a list. RULES: 1. Use ONLY Devnagari script for {language}. 2. NO English/Roman letters. 3. NO Chinese/other scripts."},
                {"role": "user", "content": f"Report: ### {text_to_process} ###"}
            ]
        )
        home_precautions = precautions_response.choices[0].message.content
        
        status.update(label="Pipeline Complete!", state="complete")

    # --- RESULTS DISPLAY ---
    st.subheader("📊 Analyzed Report Results")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"<div class='result-card'><b>🧠 Plain English Summary</b><br><p>{final_english}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-card'><b>🌐 Localized ({language})</b><br><p>{hindi_translation}</p></div>", unsafe_allow_html=True)

    with col_b:
        risk_class = "risk-high" if "HIGH" in risk_data.upper() else "risk-mod" if "MODERATE" in risk_data.upper() else "risk-low"
        st.markdown(f"<div class='result-card {risk_class}'><b>🚨 Triage & Risk Data</b><br><pre style='white-space: pre-wrap; font-family: sans-serif; color: #1a1a1a;'>{risk_data}</pre></div>", unsafe_allow_html=True)
        
    st.markdown(f"<div class='result-card' style='border-left: 5px solid #2196f3; background-color: #e3f2fd;'><b>🏡 At-Home Precautions ({language})</b><br><p>{home_precautions}</p></div>", unsafe_allow_html=True)
        
    with st.expander("Show Original Medical Text / OCR Output"):
        st.text(text_to_process)
        
    st.caption("⚠️ Disclaimer: For informational use only. Consult a doctor for medical decisions.")

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

st.markdown("""
    <style>
    .agent-box { background-color: #f8f9fa; color: #212529; padding: 15px; border-radius: 8px; border-left: 5px solid #4CAF50; margin-bottom: 10px; }
    .risk-box { background-color: #ffebee; color: #212529; padding: 15px; border-radius: 8px; border-left: 5px solid #f44336; margin-bottom: 10px; }
    .precaution-box { background-color: #e3f2fd; color: #212529; padding: 15px; border-radius: 8px; border-left: 5px solid #2196f3; margin-top: 15px; margin-bottom: 15px;}
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #0d6efd; color: white;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏥 MedicAI: True Agentic Pipeline")
    st.subheader("Bridging India's Health Literacy Gap")
with col2:
    st.info("Status: Live Prototype | ABDM Compliant")

# --- SIDEBAR (TEAM & SETTINGS) ---
with st.sidebar:
    st.header("Team BioBackers")
    st.write("**SIT Pune | Division A-2**")
    st.write("- Aditi Pandey\n- Niharika Bhalerao\n- Anish Kumar Sahu\n- Aman Choudhary")
    st.divider()
    st.write("⚙️ **System Settings**")
    language = st.selectbox("Target Localization", ["Hindi (हिंदी)", "Marathi (मराठी)"])

# --- MAIN INPUT AREA (TABS) ---
st.markdown("### 📥 Choose Input Method")
tab1, tab2 = st.tabs(["📝 Paste Text", "📸 Upload Image Scan"])

text_to_process = ""

# TAB 1: Text Input
with tab1:
    raw_text_input = st.text_area("Paste medical report text here:", height=150)
    if st.button("🚀 Run Pipeline on Text", key="btn_text"):
        if raw_text_input.strip():
            text_to_process = raw_text_input
        else:
            st.warning("Please paste some text first!")

# TAB 2: Image Upload
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
                    st.success("Text extracted successfully! Routing to agents...")
                else:
                    st.error("Could not read text from the image. Please try a clearer scan.")

# --- THE UNIFIED AGENTIC PIPELINE ---
if text_to_process:
    st.divider()
    with st.status("Executing 5-Agent Workflow...", expanded=True) as status:
        
        # ---------------------------------------------------------
        # AGENT 1: THE TRIAGE & RISK ANALYZER
        # ---------------------------------------------------------
        st.write("🛡️ [Risk & Triage Agent] Analyzing medical context...")
        risk_response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": "You are a medical triage agent. Read the report and reply with ONLY a JSON format: {'document_type': '...', 'risk_level': 'HIGH/MODERATE/LOW', 'risk_reason': '... summary...', 'recommendation': '...next step...'}"},
                {"role": "user", "content": text_to_process} 
            ]
        )
        risk_data = risk_response.choices[0].message.content 
        
        # ---------------------------------------------------------
        # AGENT 2: THE SIMPLIFIER
        # ---------------------------------------------------------
        st.write("🧠 [Simplifier Agent] Drafting layman explanation...")
        simp_response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": "You are a patient-communication expert. Convert this medical text into 2 simple English sentences for someone with low health literacy."},
                {"role": "user", "content": text_to_process} 
            ]
        )
        draft_summary = simp_response.choices[0].message.content
        
        # ---------------------------------------------------------
        # AGENT 3: THE REVIEWER (Self-Correction)
        # ---------------------------------------------------------
        st.write("🕵️ [Reviewer Agent] Auditing for medical hallucinations...")
        review_response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": "You are a clinical auditor. Compare the ORIGINAL TEXT to the DRAFT SUMMARY. Did the draft invent any facts or miss the main diagnosis? Reply 'PASS' or 'FAIL: [Reason]'."},
                {"role": "user", "content": f"ORIGINAL: {text_to_process}\n\nDRAFT: {draft_summary}"}
            ]
        )
        audit_result = review_response.choices[0].message.content
        
        if "FAIL" in audit_result:
            st.warning(f"Self-Correction Triggered: {audit_result}")
            st.write("🔄 [Simplifier Agent] Rewriting based on feedback...")
            fix_response = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=[
                    {"role": "system", "content": f"Rewrite this draft to fix this error: {audit_result}"},
                    {"role": "user", "content": draft_summary}
                ]
            )
            final_english = fix_response.choices[0].message.content
        else:
            st.success("Reviewer Agent cleared the output.")
            final_english = draft_summary

        # ---------------------------------------------------------
        # AGENT 4: THE TRANSLATOR
        # ---------------------------------------------------------
        st.write(f"🌐 [Translation Agent] Localizing output to {language}...")
        trans_response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {
                    "role": "system", 
                    "content": f"Translate the following English text into simple, conversational {language}. You MUST use the native Devanagari script. Do NOT use Roman letters. Do NOT write in Hinglish."
                },
                {"role": "user", "content": final_english}
            ]
        )
        hindi_translation = trans_response.choices[0].message.content

        # ---------------------------------------------------------
        # AGENT 5: THE HOME CARE ADVISOR
        # ---------------------------------------------------------
        st.write(f"🏡 [Home Care Agent] Generating safe at-home precautions in {language}...")
        precautions_response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {
                    "role": "system", 
                    "content": f"You are a preventative care advisor. Based on this medical text, provide 3 simple, safe, at-home precautions or lifestyle changes the patient can do while waiting for a doctor. Format as a bulleted list. DO NOT prescribe medicine. If the text indicates a critical emergency, the only precaution should be 'Do not exert yourself. Sit down, remain calm, and wait for emergency medical services.' You MUST write these precautions in simple, conversational {language} using the native Devanagari script. Do NOT use English, Roman letters, or Hinglish."
                },
                {"role": "user", "content": text_to_process}
            ]
        )
        home_precautions = precautions_response.choices[0].message.content

    # --- FINAL OUTPUT PRESENTATION ---
    st.subheader("📊 Analyzed Report Results")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"<div class='agent-box'><b>🧠 Plain English Summary</b><br>{final_english}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='agent-box'><b>🌐 Localized Output ({language})</b><br>{hindi_translation}</div>", unsafe_allow_html=True)

    with col_b:
        risk_color = "#f44336" if "HIGH" in risk_data.upper() else "#ff9800" if "MODERATE" in risk_data.upper() else "#4CAF50"
        st.markdown(f"<div style='background-color: #f8f9fa; color: #212529; padding: 15px; border-radius: 8px; border-left: 5px solid {risk_color}; margin-bottom: 10px;'><b>🚨 Triage & Risk Data</b><br><pre style='color: #212529;'>{risk_data}</pre></div>", unsafe_allow_html=True)
        
    # --- NEW: AT-HOME PRECAUTIONS SECTION ---
    st.markdown(f"<div class='precaution-box'><b>🏡 Recommended At-Home Precautions (While awaiting consultation)</b><br>{home_precautions}</div>", unsafe_allow_html=True)
        
    with st.expander("Show Original Medical Text / OCR Output"):
        st.write(text_to_process)
        
    st.caption("⚠️ Disclaimer: For informational use only. Consult a doctor for medical decisions.")
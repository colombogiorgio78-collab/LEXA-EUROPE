import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="LEXA EUROPE", page_icon="⚖️", layout="wide")
st.title("⚖️ LEXA EUROPE: Analisi Legale AI")

with st.sidebar:
    st.subheader("Configurazione AI")
    api_key = st.sidebar.text_input("Gemini API Key", type="password")
    jurisdiction = st.selectbox("Giurisdizione", ["Italia", "Unione Europea", "International"])

col_in, col_out = st.columns(2)

with col_in:
    input_mode = st.radio("Scegli modalità:", ["Carica PDF", "Incolla testo"])
    testo = ""
    if input_mode == "Carica PDF":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            testo = "".join([p.get_text() for p in doc])
    else:
        testo = st.text_area("Incolla qui il contratto:", height=300)

with col_out:
    if st.button("🚀 AVVIA ANALISI"):
        if not api_key or not testo:
            st.error("Inserisci chiave API e testo!")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Sei un avvocato. Analizza questo contratto per la legge di {jurisdiction}: \n\n {testo}"
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Errore: {e}")

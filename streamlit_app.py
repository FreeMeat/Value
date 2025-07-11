import streamlit as st
import requests
import sys
import subprocess
import time
from datetime import datetime

# Prüfen, ob BeautifulSoup installiert ist
try:
    from bs4 import BeautifulSoup
    bs4_available = True
except ImportError:
    bs4_available = False

# Elegantes schwarzes Design
st.set_page_config(
    page_title="🚀 Value Investor Pro",
    layout="centered",
    page_icon="💼"
)

# CSS für schwarzes Design
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #000000;
        color: #ffffff;
    }
    .stTextInput>div>div>input {
        background-color: #111111;
        color: #ffffff;
        border: 1px solid #333333;
    }
    .metric-card {
        background: #121212;
        border: 1px solid #333333;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6, p {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Haupt-GUI
st.title("🚀 Value Investor Pro")

# Installationsanweisung, wenn BeautifulSoup fehlt
if not bs4_available:
    st.error("""
    **Erforderliche Bibliotheken nicht installiert!**
    
    Bitte führen Sie folgenden Befehl in Ihrem Terminal aus:
    ```bash
    pip install beautifulsoup4 requests streamlit
    ```
    
    Alternativ können Sie die Bibliotheken direkt von hier installieren:
    """)
    
    if st.button("📦 Bibliotheken jetzt installieren", type="primary"):
        with st.spinner("Installiere BeautifulSoup und Requests..."):
            try:
                # Versuch, Bibliotheken zu installieren
                subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                     "beautifulsoup4", "requests", "streamlit"])
                st.success("Installation erfolgreich! Bitte starten Sie die App neu.")
                st.balloons()
            except Exception as e:
                st.error(f"Installation fehlgeschlagen: {str(e)}")
    return

# Funktionen
def get_financial_data(isin):
    try:
        url = f"https://www.onvista.de/aktien/{isin}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept-Language': 'de-DE,de;q=0.9'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Basisdaten
        name = soup.find('h1', class_='headline').get_text(strip=True) if soup.find('h1', class_='headline') else "N/A"
        price = soup.find('span', class_='price').get_text(strip=True) if soup.find('span', class_='price') else "0,00"
        
        # Metriken
        metrics = {}
        metric_keys = {
            "KGV": "KGV (aktuell)",
            "KBV": "KBV",
            "Dividendenrendite": "Dividendenrendite",
            "Eigenkapitalrendite": "Eigenkapitalrendite",
            "Marktkapitalisierung": "Marktkapitalisierung"
        }
        
        for key, value in metric_keys.items():
            element = soup.find('td', text=lambda t: t and value in t)
            metrics[key] = element.find_next_sibling('td').get_text(strip=True) if element else "N/A"
        
        return {
            "Name": name,
            "Preis": price + " €",
            **metrics
        }
        
    except Exception as e:
        st.error(f"Fehler beim Datenabruf: {str(e)}")
        return None

# Eingabebereich
st.markdown("Unternehmensbewertung mit schwarzem Design für optimale Lesbarkeit")
col1, col2 = st.columns([3,1])
with col1:
    isin = st.text_input(
        "**ISIN eingeben:**",
        placeholder="DE000BASF111",
        max_chars=15
    )
with col2:
    analyze_btn = st.button(
        "🚀 Analyse starten", 
        type="primary"
    )

# Beispiel-ISINs
st.markdown("""
<div class="metric-card">
    <h3>💡 Beispiel-ISINs</h3>
    <p><strong>BASF:</strong> DE000BASF111</p>
    <p><strong>Siemens:</strong> DE0007236101</p>
    <p><strong>Allianz:</strong> DE0008404005</p>
    <p><strong>Adidas:</strong> DE000A1EWWW0</p>
</div>
""", unsafe_allow_html=True)

# Ergebnisanzeige
if analyze_btn and isin:
    with st.spinner("Daten werden abgerufen..."):
        data = get_financial_data(isin)
        time.sleep(1.5)
        
    if data:
        st.success(f"## 📈 {data['Name']}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div>Preis</div>
                <h2>{data['Preis']}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div>KGV</div>
                <h2>{data['KGV']}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div>Dividendenrendite</div>
                <h2>{data['Dividendenrendite']}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<div style='color: #bbbbbb; text-align: right;'>Letzte Aktualisierung: {datetime.now().strftime('%d.%m.%Y %H:%M')}</div>", unsafe_allow_html=True)
        
elif analyze_btn and not isin:
    st.warning("Bitte geben Sie eine ISIN ein")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #888;">
    © 2023 Value Investor Pro | Datenquelle: OnVista
</div>
""", unsafe_allow_html=True)

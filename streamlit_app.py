import streamlit as st
import requests
import time
from datetime import datetime

# Versuchen Sie, BeautifulSoup zu importieren
try:
    from bs4 import BeautifulSoup
    bs4_available = True
except ImportError:
    bs4_available = False
    st.error("""
    **Fehlendes Modul: BeautifulSoup**  
    Bitte installieren Sie die benötigten Bibliotheken mit:  
    `pip install beautifulsoup4 requests streamlit`
    """)

# GUI-Konfiguration
st.set_page_config(
    page_title="🚀 Value Investor Pro",
    layout="centered",
    page_icon="💼"
)

# CSS für modernes Design
st.markdown("""
<style>
    /* Hauptdesign */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
    }
    
    /* Widgets */
    .stTextInput>div>div>input {
        border-radius: 12px;
        padding: 12px 15px;
        border: 1px solid #ddd;
        font-size: 16px;
    }
    
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        font-weight: bold;
        padding: 10px 24px;
        border: none;
        box-shadow: 0 4px 6px rgba(50, 152, 255, 0.3);
        transition: all 0.3s ease;
        margin-top: 15px;
    }
    
    /* Karten */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        margin: 20px 0;
        border: 1px solid #eef2f6;
    }
    
    .metric-title {
        color: #5b7083;
        font-size: 16px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .metric-value {
        color: #1da1f2;
        font-size: 28px;
        font-weight: 700;
    }
    
    /* Header */
    h1 {
        color: #1a73e8 !important;
        font-weight: 800 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Funktionen
def get_financial_data(isin):
    if not bs4_available:
        return None
        
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
            "Dividendenrendite": "Dividendenrendite"
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

# Haupt-GUI
st.title("💰 Value Investor Pro")
st.caption("Professionelle Unternehmensbewertung nach der Value-Strategie")

# Eingabebereich
col1, col2 = st.columns([3,1])
with col1:
    isin = st.text_input(
        "ISIN eingeben:",
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
**💡 Beispiele:**
- BASF: DE000BASF111
- Siemens: DE0007236101
- Allianz: DE0008404005
- Adidas: DE000A1EWWW0
""")

# Ergebnisanzeige
if analyze_btn and isin:
    if not bs4_available:
        st.error("BeautifulSoup ist nicht installiert. Bitte installieren Sie die benötigten Bibliotheken.")
    else:
        with st.spinner("Daten werden abgerufen..."):
            data = get_financial_data(isin)
            time.sleep(1.5)
            
        if data:
            # Unternehmensname
            st.success(f"## 📈 {data['Name']}")
            
            # Metriken in Karten
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Aktueller Preis</div>
                    <div class="metric-value">{data['Preis']}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">KGV</div>
                    <div class="metric-value">{data['KGV']}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Dividendenrendite</div>
                    <div class="metric-value">{data['Dividendenrendite']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # KBV anzeigen
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">KBV (Kurs-Buchwert-Verhältnis)</div>
                <div class="metric-value">{data['KBV']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Zeitstempel
            st.caption(f"Letzte Aktualisierung: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            
elif analyze_btn and not isin:
    st.warning("Bitte geben Sie eine ISIN ein")

# Erklärungen
st.markdown("---")
st.subheader("📝 Bedeutung der Kennzahlen")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>KGV (Kurs-Gewinn-Verhältnis)</h3>
        <p>Bewertet den Preis im Verhältnis zum Gewinn pro Aktie.<br>
        <strong>Value-Richtwert:</strong> Unter 15</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>KBV (Kurs-Buchwert-Verhältnis)</h3>
        <p>Zeigt das Verhältnis von Marktpreis zum Buchwert je Aktie.<br>
        <strong>Value-Richtwert:</strong> Unter 1.5</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #777;">
    © 2023 Value Investor Pro | Datenquelle: OnVista
</div>
""", unsafe_allow_html=True)

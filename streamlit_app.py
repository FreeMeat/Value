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

# GUI-Konfiguration mit schwarzem Design
st.set_page_config(
    page_title="🚀 Value Investor Pro",
    layout="centered",
    page_icon="💼"
)

# Elegantes schwarzes Design
st.markdown("""
<style>
    /* Hauptdesign - Dunkler Hintergrund */
    [data-testid="stAppViewContainer"] {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Widgets */
    .stTextInput>div>div>input {
        border-radius: 12px;
        padding: 12px 15px;
        border: 1px solid #333333;
        background-color: #111111;
        color: #ffffff;
        font-size: 16px;
    }
    
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(to right, #1a73e8 0%, #0d47a1 100%) !important;
        color: white !important;
        font-weight: bold;
        padding: 10px 24px;
        border: none;
        box-shadow: 0 4px 6px rgba(13, 71, 161, 0.4);
        transition: all 0.3s ease;
        margin-top: 15px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(13, 71, 161, 0.6);
    }
    
    /* Karten - Dunkle Karten mit hellem Text */
    .metric-card {
        background: #121212;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.5);
        margin: 20px 0;
        border: 1px solid #333333;
    }
    
    .metric-title {
        color: #bbbbbb;
        font-size: 16px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .metric-value {
        color: #1a73e8;
        font-size: 28px;
        font-weight: 700;
    }
    
    /* Header */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Allgemeine Textfarben */
    body, .stMarkdown, .st-c7, .stTextInput>div>div>label, .st-cq, .stAlert, .stWarning, .stSuccess {
        color: #ffffff !important;
    }
    
    /* Trennlinien */
    hr {
        border-color: #333333;
    }
    
    /* Platzhalter für fehlende Werte */
    .na-value {
        color: #888888;
        font-style: italic;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #333333;
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

# Haupt-GUI
st.title("🚀 Value Investor Pro")
st.markdown("Unternehmensbewertung mit schwarzem Design für optimale Lesbarkeit")

# Eingabebereich
col1, col2 = st.columns([3,1])
with col1:
    isin = st.text_input(
        "**ISIN eingeben:**",
        placeholder="DE000BASF111",
        max_chars=15,
        help="Geben Sie die ISIN des Unternehmens ein, z.B. DE000BASF111 für BASF"
    )
with col2:
    analyze_btn = st.button(
        "🚀 Analyse starten", 
        type="primary"
    )

# Beispiel-ISINs mit schwarzem Design
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
            
            # Zweite Reihe
            col4, col5, col6 = st.columns(3)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">KBV</div>
                    <div class="metric-value">{data['KBV']}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col5:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Eigenkapitalrendite</div>
                    <div class="metric-value">{data['Eigenkapitalrendite']}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col6:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Marktkapitalisierung</div>
                    <div class="metric-value">{data['Marktkapitalisierung']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Zeitstempel
            st.markdown(f"<div style='color: #bbbbbb; text-align: right;'>Letzte Aktualisierung: {datetime.now().strftime('%d.%m.%Y %H:%M')}</div>", unsafe_allow_html=True)
            
elif analyze_btn and not isin:
    st.warning("Bitte geben Sie eine ISIN ein")

# Erklärungen mit schwarzem Design
st.markdown("---")
st.subheader("📚 Bedeutung der Kennzahlen")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>KGV (Kurs-Gewinn-Verhältnis)</h3>
        <p>Bewertet den Preis im Verhältnis zum Gewinn pro Aktie.<br>
        <strong>Value-Richtwert:</strong> Unter 15</p>
    </div>
    
    <div class="metric-card">
        <h3>Dividendenrendite</h3>
        <p>Die jährliche Dividende dividiert durch den Aktienkurs.<br>
        <strong>Value-Richtwert:</strong> Über 3%</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>KBV (Kurs-Buchwert-Verhältnis)</h3>
        <p>Zeigt das Verhältnis von Marktpreis zum Buchwert je Aktie.<br>
        <strong>Value-Richtwert:</strong> Unter 1.5</p>
    </div>
    
    <div class="metric-card">
        <h3>Eigenkapitalrendite</h3>
        <p>Misst die Profitabilität des eingesetzten Eigenkapitals.<br>
        <strong>Value-Richtwert:</strong> Über 10%</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #888;">
    © 2023 Value Investor Pro | Datenquelle: OnVista | Schwarzes Design für optimale Lesbarkeit
</div>
""", unsafe_allow_html=True)

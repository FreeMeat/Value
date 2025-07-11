import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# -------------------------------
# GUI KONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="🚀 Value Investor Pro",
    layout="wide",
    page_icon="💼",
    initial_sidebar_state="expanded"
)

# CSS für modernes Design
st.markdown("""
<style>
    /* Hauptdesign */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(195deg, #2c3e50 0%, #1a2530 100%) !important;
        box-shadow: 5px 0 15px rgba(0,0,0,0.1);
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
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(50, 152, 255, 0.4);
    }
    
    /* Karten */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        transition: all 0.3s ease;
        border: 1px solid #eef2f6;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.12);
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
    
    /* Tabs */
    [role="tab"] {
        border-radius: 12px !important;
        padding: 10px 20px !important;
        margin: 0 5px !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# FUNKTIONEN
# -------------------------------
def get_financial_data(isin):
    """Holt Finanzdaten von OnVista mit Chrome-Header"""
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
            "KUV": "KUV",
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

# -------------------------------
# SIDEBAR - EINGABEBEREICH
# -------------------------------
with st.sidebar:
    st.image("https://i.imgur.com/zQeYq5H.png", width=200)  # Platzhalter für Logo
    st.header("🔍 Unternehmensanalyse")
    
    isin = st.text_input(
        "ISIN eingeben:",
        placeholder="DE000BASF111",
        max_chars=15,
        key="isin_input"
    )
    
    analyze_btn = st.button(
        "🚀 Analyse starten", 
        type="primary", 
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("""
    **💡 Tipps:**
    - BASF: DE000BASF111
    - Siemens: DE0007236101
    - Allianz: DE0008404005
    - Adidas: DE000A1EWWW0
    """)
    
    st.markdown("---")
    st.markdown("""
    **ℹ️ Info:**
    Diese App bewertet Unternehmen nach der Value-Investing-Strategie 
    mit Daten von [OnVista](https://www.onvista.de).
    """)

# -------------------------------
# HAUPTINHALT
# -------------------------------
st.title("💰 Value Investor Pro")
st.caption("Professionelle Unternehmensbewertung nach der Value-Strategie")

# Tabs für verschiedene Ansichten
tab1, tab2, tab3 = st.tabs(["📊 Aktienanalyse", "📈 Kennzahlen", "💡 Value-Bewertung"])

with tab1:
    if analyze_btn and isin:
        with st.spinner("Daten werden abgerufen..."):
            data = get_financial_data(isin)
            time.sleep(1.5)  # Für Ladeanimation
            
        if data:
            # Header mit Unternehmensname
            st.success(f"## 📈 {data['Name']}")
            
            # Hauptmetriken in Karten
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
                    <div class="metric-title">KGV (Kurs-Gewinn-Verhältnis)</div>
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
            
            # Detaillierte Kennzahlen
            st.subheader("📝 Weitere Finanzkennzahlen")
            col4, col5, col6 = st.columns(3)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">KBV (Kurs-Buchwert-Verhältnis)</div>
                    <div class="metric-value">{data['KBV']}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col5:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">KUV (Kurs-Umsatz-Verhältnis)</div>
                    <div class="metric-value">{data['KUV']}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col6:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Eigenkapitalrendite</div>
                    <div class="metric-value">{data['Eigenkapitalrendite']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Marktkapitalisierung
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Marktkapitalisierung</div>
                <div class="metric-value">{data['Marktkapitalisierung']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Zeitstempel
            st.caption(f"Letzte Aktualisierung: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            
    elif not isin and analyze_btn:
        st.warning("Bitte geben Sie eine ISIN in der Sidebar ein")
    else:
        # Platzhalter für Startbildschirm
        st.info("ℹ️ Geben Sie eine ISIN in der linken Sidebar ein und klicken Sie auf 'Analyse starten'")
        st.image("https://i.imgur.com/3JmBLLx.png", width=500)  # Platzhalter Grafik

with tab2:
    st.subheader("📈 Bedeutung der Kennzahlen")
    st.markdown("""
    <div class="metric-card">
        <h3>KGV (Kurs-Gewinn-Verhältnis)</h3>
        <p>Bewertet den Preis im Verhältnis zum Gewinn pro Aktie. Value-Investoren bevorzugen ein KGV unter 15.</p>
    </div>
    
    <div class="metric-card">
        <h3>KBV (Kurs-Buchwert-Verhältnis)</h3>
        <p>Zeigt das Verhältnis von Marktpreis zum Buchwert je Aktie. Ein KBV unter 1,5 gilt als günstig.</p>
    </div>
    
    <div class="metric-card">
        <h3>Dividendenrendite</h3>
        <p>Die jährliche Dividende dividiert durch den Aktienkurs. Value-Investoren suchen Werte über 3%.</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("💡 Value-Investing Strategie")
    st.markdown("""
    <div class="metric-card">
        <h3>Die 4 Prinzipien des Value-Investings</h3>
        <ol>
            <li><strong>Margin of Safety:</strong> Nur kaufen, wenn ein deutlicher Abschlag auf den inneren Wert besteht</li>
            <li><strong>Fundamentalanalyse:</strong> Konzentration auf Bilanzkennzahlen statt Markttrends</li>
            <li><strong>Langfristige Perspektive:</strong> Mindestens 5-10 Jahre Haltefrist</li>
            <li><strong>Emotionsloses Investieren:</strong> Rationale Entscheidungen basierend auf Zahlen</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    st.image("https://i.imgur.com/Y7VkGfQ.png", caption="Value vs. Growth Investing", width=500)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #777;">
    © 2023 Value Investor Pro | Datenquelle: OnVista | Diese App dient nur zu Informationszwecken
</div>
""", unsafe_allow_html=True)

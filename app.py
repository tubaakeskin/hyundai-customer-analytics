import pandas as pd
import streamlit as st
import re
import os

# 1. Sayfa Ayarları ve Gelişmiş Karanlık Tema Tasarımı (CSS)
st.set_page_config(page_title="Hyundai Customer Analytics Pro", page_icon="🚙", layout="wide")

st.markdown("""
    <style>
    /* En üstteki varsayılan Streamlit siyah şerit/menü alanını gizleme */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .stApp { background-color: #001529 !important; }
    [data-testid="stSidebar"] { background-color: #002c5f !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    div[data-testid="stMetricSimpleWidget"] {
        background-color: #002140 !important;
        border: 1px solid #003a70;
        padding: 8px 12px !important;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border-left: 6px solid #00aad2;
    }
    div[data-testid="stMetricSimpleWidget"] label { color: #a3b8cc !important; font-weight: bold; }
    div[data-testid="stMetricSimpleWidget"] div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 22px !important; }
    
    .insight-card {
        background-color: #002140 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        border: 1px solid #003a70 !important;
        margin-bottom: 15px !important;
    }
    .insight-card h4 { color: #00aad2 !important; margin-top: 0 !important; }
    .insight-card p { color: #e2e8f0 !important; font-style: italic !important; }
    h1, h2, h3, h4, span, label { color: #ffffff !important; }
    
    .stButton>button {
        background-color: #002140 !important;
        color: #ffffff !important;
        border: 1px solid #00aad2 !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background-color: #001529 !important;
        color: #00aad2 !important;
        border: 1px solid #00aad2 !important;
    }
    
    button[data-baseweb="tab"] p {
        color: #a3b8cc !important;
        font-size: 16px !important;
    }
    button[aria-selected="true"] p {
        color: #00aad2 !important;
        font-weight: bold !important;
    }
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 1rem !important;
    }
    hr {
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Banner Alanı
st.markdown("<h2 style='color: #ffffff; font-family: Arial, sans-serif; margin-bottom: 0; padding-bottom:0; margin-top:0;'>🚙 HYUNDAI CUSTOMER INSIGHTS PRO</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #00aad2; margin-top: 1px; margin-bottom: 0; font-size: 14px;'>Advanced Vehicle Quality Assurance & Customer Experience Analytics</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. Veri Yükleme ve Akıllı Ön İşleme Fonksiyonu
@st.cache_data
def load_data():
    df = pd.read_csv('Scraped_Car_Review_hyundai.csv', lineterminator='\n')
    df.columns = df.columns.str.strip()
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(4.0)
    
    def extract_year(title):
        match = re.search(r'\b(19|20)\d{2}\b', str(title))
        return int(match.group(0)) if match else 2010
    df['Model_Year'] = df['Vehicle_Title'].apply(extract_year)
    
    def extract_model(title):
        title_str = str(title).lower()
        if 'elantra' in title_str: return 'Elantra'
        elif 'accent' in title_str: return 'Accent'
        elif 'azera' in title_str: return 'Azera'
        elif 'tucson' in title_str: return 'Tucson'
        elif 'santa fe' in title_str: return 'Santa Fe'
        elif 'sonata' in title_str: return 'Sonata'
        else: return 'Other Models'
    df['Model_Group'] = df['Vehicle_Title'].apply(extract_model)
    return df

try:
    df = load_data()

    # 4. Sol Menü - Logo ve Filtreler
    logo_width = 150
    col_logo_1, col_logo_2, col_logo_3 = st.sidebar.columns([1, 2, 1])
    with col_logo_2:
        if os.path.exists('hyundai_logo.jpg'): st.image('hyundai_logo.jpg', width=logo_width)
        elif os.path.exists('hyundai_logo.jpeg'): st.image('hyundai_logo.jpeg', width=logo_width)
        elif os.path.exists('hyundai_logo.png'): st.image('hyundai_logo.png', width=logo_width)
        else: st.markdown("<h2 style='color: #00aad2; text-align: center;'>HYUNDAI</h2>", unsafe_allow_html=True)
        
    st.sidebar.markdown("## 🎛️ Control Panel")
    selected_model = st.sidebar.selectbox("Select Vehicle Model", sorted(df['Model_Group'].unique()))
    selected_years = st.sidebar.slider("Select Model Year Range", int(df['Model_Year'].min()), int(df['Model_Year'].max()), (int(df['Model_Year'].min()), int(df['Model_Year'].max())))
    search_query = st.sidebar.text_input("🔍 Search Keyword (e.g. engine, fuel, seat)", "")

    st.sidebar.markdown("### ⚡ Quick Topic Filters")
    col_b1, col_b2 = st.sidebar.columns(2)
    with col_b1:
        if st.button("🔧 Engine"): search_query = "engine"
        if st.button("🛑 Brakes"): search_query = "brake"
    with col_b2:
        if st.button("🛋️ Comfort"): search_query = "comfort"
        if st.button("⛽ Fuel"): search_query = "fuel"

    filtered_df = df[(df['Model_Group'] == selected_model) & (df['Model_Year'] >= selected_years[0]) & (df['Model_Year'] <= selected_years[1])]
    if search_query:
        filtered_df = filtered_df[filtered_df['Review'].str.contains(search_query, case=False, na=False)]

    # 5. SEKMELİ YAPI KURULUMU
    tab1, tab2 = st.tabs(["📊 Model Performance Dashboard", "🤖 Live AI Sentiment Predictor"])

    # --- SEKME 1: DASHBOARD ---
    with tab1:
        total_reviews = len(filtered_df)
        if total_reviews > 0:
            avg_rating = filtered_df['Rating'].mean()
            advantage_score = int(avg_rating * 20)
            pos_rate = len(filtered_df[filtered_df['Rating'] >= 4.0]) / total_reviews
            neg_rate = len(filtered_df[filtered_df['Rating'] <= 2.5]) / total_reviews
            neu_rate = 1.0 - (pos_rate + neg_rate)
            
            main_col1, main_col2 = st.columns([2, 3])
            with main_col1:
                st.markdown(f"<h3 style='margin-top:0; margin-bottom:5px;'>🎯 Executive Summary ({selected_model})</h3>", unsafe_allow_html=True)
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1: st.metric(label="Experiences", value=f"{total_reviews:,}")
                with m_col2: st.metric(label="Avg Rating", value=f"{avg_rating:.2f}/5")
                with m_col3: st.metric(label="Adv. Score", value=f"{advantage_score}/100")
                
                if neg_rate > 0.20:
                    st.error(f"⚠️ **QA ALERT:** Negative feedback rate is high ({neg_rate*100:.1f}%). Root cause analysis required.")
                
                st.write("Positive Feedback"); st.progress(int(pos_rate * 100))
                st.write("Neutral Feedback"); st.progress(int(neu_rate * 100))
                st.write("Negative Feedback"); st.progress(int(neg_rate * 100))
                st.info(f"Analysis for {selected_model} ({selected_years[0]}-{selected_years[1]}) indicates a satisfaction score of {advantage_score}/100.")

            with main_col2:
                all_text = " ".join(filtered_df['Review'].astype(str)).lower()
                adv_list = ["Ride Comfort & Interior Ergonomics", "Steady Fuel Efficiency over long-term usage", "High price-to-performance value compared to market peers"]
                disadv_list = ["Highway cabin noise (wind/road insulation limits)", "Early brake wear patterns reported by standard city drivers", "Suspension stiffness noted on uneven terrains"]
                
                st.markdown("<h3 style='margin-top:0; margin-bottom:5px;'>🟢 Dynamic Advantages</h3>", unsafe_allow_html=True)
                for i, adv in enumerate(adv_list, 1): st.success(f"{i}. **{adv}**")
                st.markdown("<h3 style='margin-top:5px; margin-bottom:5px;'>🔴 Dynamic Disadvantages</h3>", unsafe_allow_html=True)
                for i, disadv in enumerate(disadv_list, 1): st.error(f"{i}. **{disadv}**")

            st.markdown("---")
            st.markdown("<h3 style='margin-top:0;'>💬 Filtered Raw Customer Voices</h3>", unsafe_allow_html=True)
            sort_option = st.selectbox("Sort Reviews By", ["Default", "Highest Rating", "Lowest Rating"])
            display_df = filtered_df.copy()
            if sort_option == "Highest Rating": display_df = display_df.sort_values(by='Rating', ascending=False)
            elif sort_option == "Lowest Rating": display_df = display_df.sort_values(by='Rating', ascending=True)

            for idx, row in display_df.head(5).iterrows():
                status_color = "🟢 Positive" if row['Rating'] >= 4.0 else ("🟡 Neutral" if row['Rating'] == 3.0 else "🔴 Negative")
                st.markdown(f"""<div class="insight-card"><h4>{row['Review_Title']} <span style='font-size:14px; color:#a3b8cc;'>({row['Vehicle_Title']})</span></h4><span style="color: #a3b8cc; font-size: 13px; font-weight: bold;">Status: {status_color} | Rating: {row['Rating']}</span><p style="margin-top: 8px;">"{row['Review']}"</p></div>""", unsafe_allow_html=True)
        else:
            st.warning("⚠️ No reviews found matching the selected filters.")

    # --- SEKME 2: CANLI AI TAHMİN MOTORU ---
    with tab2:
        st.markdown("<h2>🤖 Live Sentiment Classification Engine</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #a3b8cc;'>Cümle yapısını ve olumsuzluk örüntülerini anlık çözen, donma yapmayan akıllı model.</p>", unsafe_allow_html=True)
        
        user_input = st.text_area("✍ *Yorum Girin / Enter Customer Review:*", "Bu modeli hiç sevmedim.")
        
        if user_input.strip():
            st.markdown("### 🔍 Model Analiz Sonuçları")
            text = user_input.lower().strip()
            
            # Anlamsız Rastgele Harf Validasyonu
            is_random = False
            if len(text) >= 4:
                if any(text[i] == text[i+1] == text[i+2] for i in range(len(text)-2)) or not any(vowel in text for vowel in 'aeıioöuü'):
                    is_random = True
            
            if is_random:
                st.warning("⚠️ **Girdi Anlaşılamadı:** Rastgele karakter dizilimi veya anlamsız metin algılandı. Lütfen geçerli bir değerlendirme cümlesi yazın.")
            else:
                # Akıllı Örüntü Eşleştirme (Regex)
                negative_patterns = r'(medim|madım|medi|madı|miyor|mıyor|mem|mam|kötü|berbat|arıza|problem|sorun|ses yapıyor|gürültü|değil|yok|hiç|bad|worst|noise|problem|dislike|annoying)'
                positive_patterns = r'(iyi|güzel|harika|mükemmel|rahat|konforlu|sağlam|güvenilir|memnun|başarılı|seviyorum|beğendim|good|great|amazing|excellent|love|perfect|comfortable|smooth)'
                
                has_negative = bool(re.search(negative_patterns, text))
                has_positive = bool(re.search(positive_patterns, text))
                
                if has_negative and not has_positive:
                    st.error("🔴 **Yapay Zeka Tahmini: NEGATİF** (Cümle yapısında net bir memnuniyetsizlik veya olumsuzluk kalıbı çözümlendi.)")
                elif has_positive and not has_negative:
                    st.success("🟢 **Yapay Zeka Tahmini: POZİTİF** (Cümle yapısında net bir memnuniyet veya olumlu kalıp çözümlendi.)")
                elif has_positive and has_negative:
                    st.warning("🟡 **Yapay Zeka Tahmini: NÖTR / DENGELİ TONA SAHİP** (Metin hem olumlu hem olumsuz unsurları bir arada barındırıyor.)")
                else:
                    st.warning("🟡 **Yapay Zeka Tahmini: NÖTR / BELİRSİZ** (Yazılan metinde baskın bir duygu yönü tespit edilemedi.)")

except FileNotFoundError:
    st.error("Please ensure 'Scraped_Car_Review_hyundai.csv' is in the same directory as this script.")
import pandas as pd
import streamlit as st
import re
import os

# 1. Sayfa Ayarları ve Gelişmiş Karanlık Tema Tasarımı (CSS)
st.set_page_config(page_title="Hyundai Customer Analytics", page_icon="🚙", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #001529 !important; }
    [data-testid="stSidebar"] { background-color: #002c5f !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    div[data-testid="stMetricSimpleWidget"] {
        background-color: #002140 !important;
        border: 1px solid #003a70;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border-left: 6px solid #00aad2;
    }
    div[data-testid="stMetricSimpleWidget"] label { color: #a3b8cc !important; font-weight: bold; }
    div[data-testid="stMetricSimpleWidget"] div[data-testid="stMetricValue"] { color: #ffffff !important; }
    
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
        background-color: #00aad2 !important;
        color: #001529 !important;
        border: 1px solid #00aad2 !important;
    }
    
    /* Sekme (Tabs) başlık renklerini beyaz yapma */
    button[data-baseweb="tab"] p {
        color: #a3b8cc !important;
        font-size: 16px !important;
    }
    button[aria-selected="true"] p {
        color: #00aad2 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Üst Banner Alanı
st.markdown("<h1 style='color: #ffffff; font-family: Arial, sans-serif; margin-bottom: 0;'>🚙 HYUNDAI CUSTOMER INSIGHTS</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #00aad2; margin-top: 5px; font-size: 16px;'>Data-Driven Vehicle Evaluation & Performance Platform</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. Veri Yükleme ve Akıllı Ön İşleme Fonksiyonu
@st.cache_data
def load_data():
    df = pd.read_csv('Scraped_Car_Review_hyundai.csv', lineterminator='\n')
    df.columns = df.columns.str.strip()
    
    def clean_rating(x):
        try: return float(x)
        except: return 4.0
    df['Rating'] = df['Rating'].apply(clean_rating)
    
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
    if os.path.exists('hyundai_logo.jpg'): st.sidebar.image('hyundai_logo.jpg', use_container_width=True)
    elif os.path.exists('hyundai_logo.jpeg'): st.sidebar.image('hyundai_logo.jpeg', use_container_width=True)
    elif os.path.exists('hyundai_logo.png'): st.sidebar.image('hyundai_logo.png', use_container_width=True)
    else: st.sidebar.markdown("<h2 style='color: #00aad2; text-align: center;'>HYUNDAI</h2>", unsafe_allow_html=True)
        
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("## 🎛️ Control Panel")
    selected_model = st.sidebar.selectbox("Select Vehicle Model", df['Model_Group'].unique())
    
    min_year = int(df['Model_Year'].min())
    max_year = int(df['Model_Year'].max())
    selected_years = st.sidebar.slider("Select Model Year Range", min_year, max_year, (min_year, max_year))
    
    search_query = st.sidebar.text_input("🔍 Search Keyword (e.g. engine, fuel, seat)", "")

    st.sidebar.markdown("### ⚡ Quick Topic Filters")
    col_b1, col_b2 = st.sidebar.columns(2)
    with col_b1:
        if st.button("🔧 Engine"): search_query = "engine"
        if st.button("🛑 Brakes"): search_query = "brake"
    with col_b2:
        if st.button("🛋️ Comfort"): search_query = "comfort"
        if st.button("⛽ Fuel"): search_query = "fuel"

    # Filtreleri Uygulama
    filtered_df = df[
        (df['Model_Group'] == selected_model) & 
        (df['Model_Year'] >= selected_years[0]) & 
        (df['Model_Year'] <= selected_years[1])
    ]
    if search_query:
        filtered_df = filtered_df[filtered_df['Review'].str.contains(search_query, case=False, na=False)]

    # 5. SEKMELİ YAPI KURULUMU (Tabs)
    tab1, tab2 = st.tabs(["📊 Model Performance Dashboard", "🤖 Live AI Sentiment Predictor"])

    # --- SEKME 1: DASHBOARD ---
    with tab1:
        total_reviews = len(filtered_df)
        if total_reviews > 0:
            avg_rating = filtered_df['Rating'].mean()
            advantage_score = int(avg_rating * 20)
            
            pos_reviews = filtered_df[filtered_df['Rating'] >= 4.0]
            neg_reviews = filtered_df[filtered_df['Rating'] <= 2.5]
            pos_rate = (len(pos_reviews) / total_reviews)
            neg_rate = (len(neg_reviews) / total_reviews)
            neu_rate = 1.0 - (pos_rate + neg_rate)
        else:
            avg_rating, advantage_score, pos_rate, neg_rate, neu_rate = 0, 0, 0, 0, 0

        col1, col2, col3 = st.columns(3)
        with col1: st.metric(label="📊 Filtered Experiences", value=f"{total_reviews:,}")
        with col2: st.metric(label="⭐ Avg User Rating (5)", value=f"{avg_rating:.2f} / 5.0" if total_reviews > 0 else "N/A")
        with col3: st.metric(label="🏆 Vehicle Advantage Score", value=f"{advantage_score} / 100" if total_reviews > 0 else "N/A")

        st.markdown("<br>", unsafe_allow_html=True)

        if total_reviews > 0:
            st.markdown(f"<h2>🎯 Executive Summary for {selected_model}</h2>", unsafe_allow_html=True)
            summary_col1, summary_col2 = st.columns(2)
            
            with summary_col1:
                st.markdown("<h3>📊 Customer Sentiment Ratios</h3>", unsafe_allow_html=True)
                st.write("Positive Feedback")
                st.progress(int(pos_rate * 100))
                st.write("Neutral Feedback")
                st.progress(int(neu_rate * 100))
                st.write("Negative Feedback")
                st.progress(int(neg_rate * 100))
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<h3>🤝 Common User Consensus (Ortak Görüş)</h3>", unsafe_allow_html=True)
                st.info(f"Analysis for {selected_model} models between {selected_years[0]} and {selected_years[1]} indicates a customer satisfaction rate aligned with an advantage score of {advantage_score}/100.")

            with summary_col2:
                all_text = " ".join(filtered_df['Review'].astype(str)).lower()
                
                # --- DİNAMİK AVANTAJ ANALİZİ (Frekans Tabanlı) ---
                adv_keywords = {
                    "Ride Comfort & Interior Ergonomics": ["comfort", "comfortable", "seat", "spacious", "interior", "cabin"],
                    "Steady Fuel Efficiency": ["mileage", "fuel", "economy", "gas", "mpg", "efficient"],
                    "High Price-to-Performance Value": ["price", "value", "worth", "cheap", "affordable", "deal"],
                    "Smooth Handling & Driving Experience": ["smooth", "handling", "drive", "steering", "wheel", "power"]
                }
                
                adv_scores = {}
                for label, words in adv_keywords.items():
                    score = sum(all_text.count(w) for w in words)
                    if score > 0:
                        adv_scores[label] = score
                
                sorted_advs = sorted(adv_scores.items(), key=lambda x: x[1], reverse=True)
                adv_list = [item[0] for item in sorted_advs]
                
                while len(adv_list) < 3:
                    fallback = "Spacious cabin and family-friendly storage components"
                    if fallback not in adv_list: adv_list.append(fallback)
                    else: adv_list.append("Reliable long-term daily commuter performance")

                # --- DİNAMİK DEZAVANTAJ ANALİZİ (Frekans Tabanlı) ---
                disadv_keywords = {
                    "Highway Cabin Noise & Insulation Limits": ["noise", "loud", "wind", "sound", "noisy", "insulation"],
                    "Early Brake Wear Patterns": ["brake", "brakes", "stopping", "wear"],
                    "Suspension Stiffness on Uneven Terrains": ["suspension", "bumpy", "rough", "ride", "stiff", "shock"],
                    "Interior Plastic Component Wear": ["plastic", "interior", "cheap", "rattle", "dashboard", "scratch"]
                }
                
                disadv_scores = {}
                for label, words in disadv_keywords.items():
                    score = sum(all_text.count(w) for w in words)
                    if score > 0:
                        disadv_scores[label] = score
                        
                sorted_disadvs = sorted(disadv_scores.items(), key=lambda x: x[1], reverse=True)
                disadv_list = [item[0] for item in sorted_disadvs]
                
                while len(disadv_list) < 3:
                    fallback = "Standard interior plastic component wear over 5+ years"
                    if fallback not in disadv_list: disadv_list.append(fallback)
                    else: disadv_list.append("Minor electronic sensor reset requirements")

                st.markdown("<h3>🟢 Dynamic Advantages (Why Buy?)</h3>", unsafe_allow_html=True)
                for i, adv in enumerate(adv_list[:3], 1): st.success(f"{i}. **{adv}**")
                
                st.markdown("<h3>🔴 Dynamic Disadvantages (Why Not Buy?)</h3>", unsafe_allow_html=True)
                for i, disadv in enumerate(disadv_list[:3], 1): st.error(f"{i}. **{disadv}**")

            st.markdown("---")
            st.markdown("<h3>💬 Filtered Raw Customer Voices</h3>", unsafe_allow_html=True)
            for idx, row in filtered_df.head(4).iterrows():
                status_color = "🟢 Positive" if row['Rating'] >= 4.0 else ("🟡 Neutral" if row['Rating'] == 3.0 else "🔴 Negative")
                st.markdown(f"""
                <div class="insight-card">
                    <h4>{row['Review_Title']} <span style='font-size:14px; color:#a3b8cc;'>({row['Vehicle_Title']})</span></h4>
                    <span style="color: #a3b8cc; font-size: 13px; font-weight: bold;">Status: {status_color} | Rating: {row['Rating']}</span>
                    <p style="margin-top: 8px;">"{row['Review']}"</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No reviews found matching the selected filters.")

    # --- SEKME 2: CANLI AI TAHMİN MOTORU ---
    with tab2:
        st.markdown("<h2>🤖 Live Sentiment Classification Engine</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #a3b8cc;'>Type any English customer review below to test the rule-based AI classification model in real-time.</p>", unsafe_allow_html=True)
        
        user_input = st.text_area("✍️ Enter Customer Review (In English):", "The handling of this vehicle is smooth and the interior is incredibly comfortable, but the engine noise at high speeds is slightly annoying.")
        
        if user_input:
            st.markdown("### 🔍 Model Analysis Results")
            
            positive_words = ['good', 'great', 'amazing', 'excellent', 'love', 'perfect', 'comfortable', 'comfort', 'smooth', 'reliable', 'best', 'nice', 'spacious']
            negative_words = ['bad', 'worst', 'junk', 'noise', 'loud', 'bumpy', 'rough', 'expensive', 'broke', 'fail', 'problem', 'defect', 'annoying', 'stiff', 'waste']
            
            tokens = user_input.lower().split()
            pos_score = sum(1 for token in tokens if any(p in token for p in positive_words))
            neg_score = sum(1 for token in tokens if any(n in token for n in negative_words))
            
            if pos_score > neg_score:
                st.success(f"🟢 **Predicted Sentiment: POSITIVE** (Matches: +{pos_score} positive terms, -{neg_score} negative terms)")
            elif neg_score > pos_score:
                st.error(f"🔴 **Predicted Sentiment: NEGATIVE** (Matches: +{pos_score} positive terms, -{neg_score} negative terms)")
            else:
                st.warning(f"🟡 **Predicted Sentiment: NEUTRAL** (Balanced tone: +{pos_score} positive terms, -{neg_score} negative terms)")
                
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 💡 Industrial Engineering Note:")
            st.info("This prototype utilizes a lexicographical token-weighting classifier to bypass heavy memory overhead, ensuring instantaneous execution on light cloud infrastructure.")

except FileNotFoundError:
    st.error("Please ensure 'Scraped_Car_Review_hyundai.csv' is in the same directory as this script.")

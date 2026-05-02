# ================================
# 📌 IMPORT LIBRARIES
# ================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# import scoring functions
from utils.scoring import *

# ================================
# 📌 PAGE CONFIG
# ================================
st.set_page_config(page_title="Real Estate Advisor", layout="wide")

# ================================
# 🎨 BACKGROUND (GITHUB IMAGE)
# ================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(15,61,62,0.9), rgba(15,61,62,0.9)),
                url("https://raw.githubusercontent.com/kirthikalakshmi/Real_Estate_Investment/main/image.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.card {
    background: rgba(19, 111, 99, 0.6);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}

h1, h2, h3 {
    color: #E8F6F3;
}

[data-testid="stMetric"] {
    background: rgba(19, 111, 99, 0.7);
    padding: 10px;
    border-radius: 10px;
}

button {
    background-color: #00C2A8 !important;
    color: black !important;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================================
# 📌 LOAD DATA
# ================================
df = pd.read_csv("cleaned_data.csv")
city_avg_price = df.groupby('City')['Price_in_Lakhs'].mean().to_dict()

# ================================
# 🏡 GLOBAL HEADER
# ================================
st.markdown("""
<h1 style='text-align: center; color: #E8F6F3;'>🏡 Real Estate Investment Analyzer</h1>
<hr style='border: 1px solid rgba(255,255,255,0.2);'>
""", unsafe_allow_html=True)

# ================================
# 📌 TABS
# ================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Overview",
    "🔮 Prediction Lab",
    "📊 Market Insights",
    "📈 Investment Simulator"
])

# ================================
# 🏠 TAB 1
# ================================
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Price", f"{df['Price_in_Lakhs'].mean():.2f} Lakhs")
    col2.metric("Max Price", f"{df['Price_in_Lakhs'].max():.2f} Lakhs")
    col3.metric("Total Properties", len(df))

    st.markdown('</div>', unsafe_allow_html=True)

# ================================
# 🔮 TAB 2
# ================================
with tab2:
    st.header("🔮 Property Prediction")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox("City", df['City'].unique())
        bhk = st.slider("BHK", 1, 5)
        size = st.number_input("Size (sqft)", 500, 5000, key="size_pred")
        price = st.number_input("Price (Lakhs)", 10, 500, key="price_pred")
        age = st.slider("Property Age", 0, 30)
        amenities = st.slider("Amenities Count", 0, 10)
        access = st.slider("Accessibility Score", 0, 20)

        predict_btn = st.button("🚀 Analyze Investment")

    with col2:
        if predict_btn:
            score = investment_score(price, city, bhk, size, amenities, access, age, city_avg_price)
            future = future_price(price, city, score)

            st.metric("Investment Score", f"{score}/100")
            st.metric("Future Price", f"{future:.2f} Lakhs")

            st.subheader("📌 Insights")
            if price < city_avg_price.get(city, price):
                st.write("✔ Price below city average")
            if amenities > 5:
                st.write("✔ Good amenities")
            if age < 10:
                st.write("✔ New property")

    st.markdown('</div>', unsafe_allow_html=True)

# ================================
# 📊 TAB 3
# ================================
with tab3:
    st.header("📊 Market Insights")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Top Cities
    st.subheader("🏙 Top 10 Cities by Avg Price")

    city_price = df.groupby('City')['Price_in_Lakhs'].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.barh(city_price.index, city_price.values)

    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    ax.tick_params(colors='white')

    st.pyplot(fig)

    # BHK Distribution
    st.subheader("🏠 BHK Distribution")

    bhk_counts = df['BHK'].value_counts().sort_index()

    fig, ax = plt.subplots()
    ax.bar(bhk_counts.index.astype(str), bhk_counts.values)

    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    ax.tick_params(colors='white')

    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# ================================
# 📈 TAB 4
# ================================
with tab4:
    st.header("📈 Investment Simulator")

    base_price = st.number_input("Enter Price", 10, 500, key="sim_price")
    growth_rate = st.slider("Growth Rate (%)", 1, 20) / 100
    years = st.slider("Years", 1, 10)

    values = []
    current = base_price

    for _ in range(years):
        current *= (1 + growth_rate)
        values.append(current)

    fig, ax = plt.subplots()
    ax.plot(values)

    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    ax.tick_params(colors='white')

    st.pyplot(fig)

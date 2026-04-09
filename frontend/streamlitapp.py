import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8000"

st.title("🇺🇸 TrumpPulse Dashboard")

# =========================
# SYSTEM STATUS
# =========================
st.header("⚙️ System Health")

try:
    res = requests.get(API)
    if res.status_code == 200:
        st.success("API is running ✅")
    else:
        st.error("API issue ❌")
except:
    st.error("API not reachable ❌")


# =========================
# SENTIMENT PIE
# =========================
st.header("📊 Sentiment Analysis")

res = requests.get(f"{API}/sentiments")
data = res.json()

df = pd.DataFrame(data)

counts = df["label"].value_counts()

st.write("Distribution:")
st.dataframe(counts)

st.pyplot(counts.plot.pie(autopct="%1.1f%%").figure)


# =========================
# QA
# =========================
st.header("❓ Ask Trump")

query = st.text_input("Ask something:")

if st.button("Ask"):
    res = requests.get(f"{API}/qa", params={"query": query})
    answers = res.json()

    for a in answers:
        st.write("-", a)
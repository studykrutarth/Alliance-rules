import streamlit as st
import pandas as pd

st.set_page_config(page_title="Alliance & NAP Rules", layout="wide")

st.title("📜 Alliance & NAP Rules")

# Replace with your Google Sheet CSV export link
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjTQe7949UoJsHJkQseRFNHfLxjDea7oE0ASbkn3p-zCBJoABDZ33pYUK_kR8nGJcxoI2PrWjIWKaF/pub?output=csv"

# Example NAP alliances list (hardcoded, or load from sheet if you want)
nap_alliances = ["WCE", "VRG", "SUP", "QAP", "SLG", "PHA", "WOW", "420", "RKS", "GOD", "HPF Happy Farms"]

# -----------------------
# Sidebar for NAP Alliances
# -----------------------
st.sidebar.header("🤝 NAP Alliances")
if nap_alliances:
    for name in nap_alliances:
        st.sidebar.write(f"- {name}")
else:
    st.sidebar.info("No NAP alliances listed yet.")

# -----------------------
# Load Rules
# -----------------------
try:
    df = pd.read_csv(sheet_url, dtype=str).fillna("")


    # Tag selector
    st.markdown("### 🏷️ Choose which rules to view:")
    choice = st.radio("", ["🤝 NAP Rules", "🏰 Alliance Rules"], horizontal=True)

    # Filter by category
    if choice == "🤝 NAP Rules":
        nap_rules = df[df["Category"].str.lower() == "nap"]
        st.header("🤝 NAP Rules")
        if not nap_rules.empty:
            for _, row in nap_rules.iterrows():
                st.subheader(row["Rule Title"])
                # preserve multiple lines
                st.markdown(row["Description"].replace("\n", "  \n"))
        else:
            st.info("No NAP rules found.")

    elif choice == "🏰 Alliance Rules":
        alliance_rules = df[df["Category"].str.lower() == "alliance"]
        st.header("🏰 Alliance Rules")
        if not alliance_rules.empty:
            for _, row in alliance_rules.iterrows():
                st.subheader(row["Rule Title"])
                # preserve multiple lines
                st.markdown(row["Description"].replace("\n", "  \n"))
        else:
            st.info("No Alliance rules found.")

except Exception as e:
    st.error("⚠️ Could not load Google Sheet. Check the link.")
    st.exception(e)

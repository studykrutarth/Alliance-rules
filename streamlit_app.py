import streamlit as st
import pandas as pd


# Use st.cache_data to load data only once
@st.cache_data
def load_data(url):
    """Loads data from a Google Sheet URL and returns a DataFrame."""
    try:
        df = pd.read_csv(url)
        # Standardize the 'Category' column to lowercase for reliable filtering
        if "Category" in df.columns:
            df["Category"] = df["Category"].str.strip().str.lower()
            return df
        else:
            st.error("⚠️ The sheet must have a 'Category' column.")
            return None
    except Exception as e:
        print(e)  # For debugging in console
        return None


def display_rules(df, category_name, header):
    """Filters and displays rules for a given category as plain text."""
    rules = df[df["Category"] == category_name]
    st.header(header)

    if not rules.empty:
        for _, row in rules.iterrows():
            # Display the title as a subheader
            st.subheader(f"📜 {row['Rule Title']}")
            # Display the description as plain text (markdown)
            st.markdown(row["Description"])
            # Optional: Add a separator for better readability between rules
            st.markdown("---")
    else:
        st.info(f"No rules found for the '{category_name.capitalize()}' category.")


# --- Page Configuration ---
st.set_page_config(
    page_title="Alliance & NAP Rules",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Source ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjTQe7949UoJsHJkQseRFNHfLxjDea7oE0ASbkn3p-zCBJoABDZ33pYUK_kR8nGJcxoI2PrWjIWKaF/pub?output=csv"
NAP_ALLIANCES = ["WCE", "VRG", "SUP", "QAP", "SLG", "PHA", "WOW", "420", "RKS", "GOD", "HPF Happy Farms"]

# --- Sidebar ---
with st.sidebar:
    st.title("🤝 NAP Alliances")
    st.markdown("The following alliances are part of the Non-Aggression Pact (NAP):")
    if NAP_ALLIANCES:
        # Use columns for a cleaner look if the list gets long
        col1, col2 = st.columns(2)
        mid_point = len(NAP_ALLIANCES) // 2 + len(NAP_ALLIANCES) % 2
        with col1:
            for name in NAP_ALLIANCES[:mid_point]:
                st.markdown(f"- `{name}`")
        with col2:
            for name in NAP_ALLIANCES[mid_point:]:
                st.markdown(f"- `{name}`")
    else:
        st.info("No NAP alliances are listed.")
    st.markdown("---")
 

# --- Main Page ---
st.title("📜 Alliance & NAP Rules")
st.markdown("---")

# --- Load Data ---
with st.spinner("Fetching the latest rules..."):
    rules_df = load_data(SHEET_URL)

if rules_df is None:
    st.error("❌ **Could not load rules.** Please check the Google Sheet link and ensure it's published correctly.")
else:
    st.success("✅ Rules loaded successfully!")

    # --- Rule Selector ---
    st.markdown("### 🏷️ Choose which rules to view:")
    choice = st.radio(
        "Select a rule category:",
        [ "🔰 New Member Rules","🤝 NAP Rules", "🏰 Alliance Rules"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # --- Display Rules ---
    if choice == "🤝 NAP Rules":
        display_rules(rules_df, "nap", "🤝 Non-Aggression Pact (NAP) Rules")
    elif choice == "🏰 Alliance Rules":
        display_rules(rules_df, "alliance", "🏰 Internal Alliance Rules")
    elif choice == "🔰 New Member Rules":
        display_rules(rules_df, "newmember", "🔰 Rules for New Members")

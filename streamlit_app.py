import streamlit as st
import pandas as pd



# Use st.cache_data to load data only once
@st.cache_data
def load_data(url):
    """Loads data from a Google Sheet URL and returns a DataFrame."""
    try:
        df = pd.read_csv(url)
        if "Category" in df.columns:
            df["Category"] = df["Category"].str.strip().str.lower()
            return df
        else:
            st.error("⚠️ The sheet must have a 'Category' column.")
            return None
    except Exception as e:
        print(e)
        return None


# This function displays content from the correct language columns
def display_rules(df, category_name, header, title_col, desc_col):
    """Filters and displays rules for a given category in the selected language."""
    rules = df[df["Category"] == category_name]
    st.header(header)

    if not rules.empty:
        for _, row in rules.iterrows():
            # Fallback to default English if a translation is missing in the sheet
            rule_title = row[title_col] if pd.notna(row[title_col]) else row["Rule Title"]
            description = row[desc_col] if pd.notna(row[desc_col]) else row["Description"]

            st.subheader(f"📜 {rule_title}")
            st.markdown(description)
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
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTdeCuHt2ILatPX7la48DIoUotPouNakqGB7Qx6uhxmXFvv06_FNeu-nVLFc0hNPGs92a0YPhSdlfNl/pub?output=csv"
NAP_ALLIANCES = ["WCE", "VRG", "SUP", "QAP", "SLG", "PHA", "WOW", "420", "RKS", "GOD", "HPF Happy Farms"]

# --- Sidebar ---
with st.sidebar:
    st.title("🤝 NAP Alliances")
    st.markdown("Alliances in our Non-Aggression Pact (NAP):")
    if NAP_ALLIANCES:
        col1, col2 = st.columns(2)
        mid_point = len(NAP_ALLIANCES) // 2 + len(NAP_ALLIANCES) % 2
        with col1:
            for name in NAP_ALLIANCES[:mid_point]: st.markdown(f"- `{name}`")
        with col2:
            for name in NAP_ALLIANCES[mid_point:]: st.markdown(f"- `{name}`")
    else:
        st.info("No NAP alliances listed.")
    st.markdown("---")

    # Language Selector with your requested languages
    st.header("🌐 Language Selection")
    language = st.selectbox(
        "Choose your language",
        ["English", "German", "French", "Chinese", "Spanish"]
    )
    st.markdown("---")
    st.info("This app displays rules sourced directly from a shared Google Sheet.")

# --- Main Page ---
st.title("📜 Alliance & NAP Rules")
st.markdown("---")

# --- Load Data ---
with st.spinner("Fetching rules..."):
    rules_df = load_data(SHEET_URL)

if rules_df is None:
    st.error("❌ **Could not load rules.** Please check the Google Sheet link and ensure it's published correctly.")
else:
    st.success("✅ Rules loaded successfully!")

    # Map the selected language to the correct column names from your sheet
    if language == "English":
        title_column = "Rule Title"
        desc_column = "Description"
    else:
        title_column = f"Rule Title_{language}"
        desc_column = f"Description_{language}"

    # --- Rule Selector ---
    choice = st.radio(
        "Select a rule category:",
        ["🔰 New Member Rules", "🤝 NAP Rules", "🏰 Alliance Rules"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown("---")

    # Pass the selected language columns to the display function
    if choice == "🔰 New Member Rules":
        display_rules(rules_df, "newmember", "🔰 Rules for New Members", title_column, desc_column)
    elif choice == "🤝 NAP Rules":
        display_rules(rules_df, "nap", "🤝 Non-Aggression Pact (NAP) Rules", title_column, desc_column)
    elif choice == "🏰 Alliance Rules":
        display_rules(rules_df, "alliance", "🏰 Internal Alliance Rules", title_column, desc_column)

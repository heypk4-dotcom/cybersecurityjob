import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title="Cyber Security Job Hunter", page_icon="🛡️", layout="wide")

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "jobs.csv")

st.title("🛡️ Cyber Security Job Hunter Dashboard")

@st.cache_data
def load_data():
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    df = pd.read_csv(CSV_PATH)
    # Convert date_posted to datetime
    if 'date_posted' in df.columns:
        df['date_posted'] = pd.to_datetime(df['date_posted'])
    return df

df = load_data()

if df.empty:
    st.warning("No job data found. Please run the scraper pipeline first.")
else:
    # Sidebar Filters
    st.sidebar.header("Filter Jobs")
    
    min_score = st.sidebar.slider("Minimum AI Match Score", 0, 100, 50)
    
    locations = df['location'].dropna().unique().tolist()
    selected_locations = st.sidebar.multiselect("Locations", locations, default=locations)
    
    companies = df['company'].dropna().unique().tolist()
    selected_companies = st.sidebar.multiselect("Companies", companies, default=companies)
    
    # Apply Filters
    filtered_df = df[
        (df['ai_score'] >= min_score) &
        (df['location'].isin(selected_locations) if selected_locations else True) &
        (df['company'].isin(selected_companies) if selected_companies else True)
    ]
    
    st.subheader(f"Found {len(filtered_df)} matching jobs")
    
    # Display Jobs
    for index, row in filtered_df.sort_values(by='ai_score', ascending=False).iterrows():
        with st.expander(f"{row['title']} @ {row['company']} (Score: {row.get('ai_score', 0)})"):
            st.markdown(f"**Location:** {row['location']}")
            st.markdown(f"**Posted:** {row['date_posted']}")
            st.markdown(f"**Key Skills Extracted:** {row.get('key_skills', 'N/A')}")
            st.markdown("### AI Summary")
            st.write(row.get('ai_summary', 'No summary available.'))
            st.markdown("### Full Description")
            st.write(row.get('description', 'No description available.'))
            st.markdown(f"[Apply / View Original Post]({row['link']})")

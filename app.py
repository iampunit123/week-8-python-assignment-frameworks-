import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Cache data so it doesn’t reload each time
@st.cache_data
def load_data(nrows=5000):  # load only first 5000 rows
    return pd.read_csv("metadata.csv", nrows=nrows)

# Load dataset
df = load_data()

st.title("CORD-19 Metadata Dashboard (Sample Data)")

# Convert publish_time to year
df["year"] = pd.to_datetime(df["publish_time"], errors="coerce").dt.year

# Sidebar filters
st.sidebar.header("Filters")

# Year filter
min_year = int(df["year"].min())
max_year = int(df["year"].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Journal filter
journals = df["journal"].dropna().unique()
selected_journal = st.sidebar.selectbox("Select Journal (optional)", ["All"] + list(journals))

# Apply filters
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
if selected_journal != "All":
    filtered_df = filtered_df[filtered_df["journal"] == selected_journal]

# Data Preview
st.subheader("Filtered Data Preview")
st.write(filtered_df.head())

# Download button for filtered data
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="filtered_metadata.csv",
    mime="text/csv",
)

# Publications by Year
st.subheader("Publications by Year")
yearly = filtered_df["year"].value_counts().sort_index()

fig, ax = plt.subplots()
sns.barplot(x=yearly.index, y=yearly.values, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Heatmap of publications per journal per year
st.subheader("Heatmap: Publications per Journal per Year")
journal_year = (
    filtered_df.groupby(["journal", "year"]).size().unstack(fill_value=0)
)
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(journal_year, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# Word Cloud of titles
st.subheader("Word Cloud of Paper Titles")
titles = " ".join(filtered_df["title"].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles)

fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)


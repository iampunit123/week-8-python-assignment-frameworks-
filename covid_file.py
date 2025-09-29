# covid_file.py
# Step 1: Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Load the dataset (only first 10,000 rows to avoid memory errors)
df = pd.read_csv("metadata.csv", nrows=10000)

# Step 3: Basic exploration
print("\n--- Basic Info ---")
print("Shape of dataset:", df.shape)   # rows and columns
print("\nColumn names:\n", df.columns) # all available columns
print("\nDataset info:\n")
print(df.info())

# Step 4: Look at the first few rows
print("\n--- First 5 Rows ---")
print(df.head())

# Step 5: Check for missing values
print("\n--- Missing Values ---")
print(df.isnull().sum().head(20))  # show missing counts for first 20 columns

# Step 6: Basic statistics (only for numeric columns)
print("\n--- Summary Statistics ---")
print(df.describe())
# ----------------------------
# Step 3: Data Cleaning
# ----------------------------

# Keep only useful columns
useful_cols = ["title", "abstract", "publish_time", "authors", "journal", "source_x"]
df = df[useful_cols]

print("\n--- Selected Columns ---")
print(df.head())

# Handle missing values: drop rows with no title or publish_time
df = df.dropna(subset=["title", "publish_time"])

# Fill missing abstracts with empty string
df["abstract"] = df["abstract"].fillna("")

# Convert publish_time to datetime format
df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")

# Drop rows where publish_time could not be parsed
df = df.dropna(subset=["publish_time"])

# Extract year for analysis
df["year"] = df["publish_time"].dt.year

# Create a simple feature: abstract word count
df["abstract_word_count"] = df["abstract"].apply(lambda x: len(str(x).split()))

print("\n--- Cleaned Data Sample ---")
print(df.head())

print("\n--- Dataset After Cleaning ---")
print(df.info())
# ----------------------------
# Step 4: Enhanced Data Analysis & Visualization
# ----------------------------
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np

# Set a nicer style with better aesthetics
sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['font.family'] = 'DejaVu Sans'  # Better font support

def create_publications_by_year(df):
    """Create enhanced publications by year plot"""
    year_counts = df["year"].value_counts().sort_index()
    
    # Filter out invalid years if any
    year_counts = year_counts[year_counts.index > 2000]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Use line plot with markers for better trend visualization
    plt.plot(year_counts.index, year_counts.values, marker='o', linewidth=3, 
             markersize=8, color='#2E86AB', alpha=0.8)
    
    # Add area fill under the line
    plt.fill_between(year_counts.index, year_counts.values, alpha=0.3, color='#2E86AB')
    
    plt.title("COVID-19 Publications Trend by Year", fontsize=18, weight="bold", pad=20)
    plt.xlabel("Year", fontsize=14, weight="bold")
    plt.ylabel("Number of Papers", fontsize=14, weight="bold")
    
    # Add value annotations
    for year, count in year_counts.items():
        plt.annotate(f'{count:,}', (year, count), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=10, weight='bold')
    
    # Improve grid and ticks
    plt.grid(True, alpha=0.3)
    plt.xticks(year_counts.index, rotation=45)
    
    plt.tight_layout()
    plt.savefig("publications_by_year.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved enhanced plot: publications_by_year.png")

def create_publications_heatmap(df):
    """Create publications heatmap with better styling"""
    df["month"] = df["publish_time"].dt.month
    heatmap_data = df.groupby(["year", "month"]).size().unstack(fill_value=0)
    
    # Filter valid years
    heatmap_data = heatmap_data[heatmap_data.index > 2000]
    
    # Create month names for better readability
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    sns.heatmap(heatmap_data, cmap="YlOrRd", annot=True, fmt="d", 
                cbar=True, linewidths=0.5, linecolor='gray',
                annot_kws={"size": 9, "weight": "bold"})
    
    plt.title("Monthly Publications Heatmap (Year vs Month)", 
              fontsize=16, weight="bold", pad=20)
    plt.xlabel("Month", fontsize=12, weight="bold")
    plt.ylabel("Year", fontsize=12, weight="bold")
    
    # Set month labels if we have all months
    if heatmap_data.shape[1] == 12:
        ax.set_xticklabels(month_names)
    
    plt.tight_layout()
    plt.savefig("publications_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved enhanced plot: publications_heatmap.png")

def create_top_journals(df):
    """Create top journals plot with improved layout"""
    top_journals = df["journal"].value_counts().head(15).sort_values(ascending=True)
    
    # Clean journal names (shorten if too long)
    top_journals.index = [name[:50] + '...' if len(name) > 50 else name 
                         for name in top_journals.index]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(range(len(top_journals)), top_journals.values, 
                   color=plt.cm.Greens(np.linspace(0.4, 0.8, len(top_journals))))
    
    plt.title("Top 15 Journals Publishing COVID-19 Research", 
              fontsize=16, weight="bold", pad=20)
    plt.xlabel("Number of Papers", fontsize=12, weight="bold")
    plt.ylabel("Journal", fontsize=12, weight="bold")
    
    # Set y-axis labels
    plt.yticks(range(len(top_journals)), top_journals.index, fontsize=10)
    
    # Add value labels on bars
    for i, (value, bar) in enumerate(zip(top_journals.values, bars)):
        width = bar.get_width()
        ax.text(width + (max(top_journals.values) * 0.01), bar.get_y() + bar.get_height()/2,
                f'{value:,}', ha='left', va='center', fontsize=9, weight='bold')
    
    plt.tight_layout()
    plt.savefig("top_journals.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved enhanced plot: top_journals.png")

def create_top_sources(df):
    """Create top sources plot with enhanced visualization"""
    top_sources = df["source_x"].value_counts().head(12).sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.Reds(np.linspace(0.4, 0.8, len(top_sources)))
    bars = ax.barh(range(len(top_sources)), top_sources.values, color=colors)
    
    plt.title("Top 12 Sources of COVID-19 Papers", fontsize=16, weight="bold", pad=20)
    plt.xlabel("Number of Papers", fontsize=12, weight="bold")
    plt.ylabel("Source", fontsize=12, weight="bold")
    
    plt.yticks(range(len(top_sources)), top_sources.index, fontsize=10)
    
    # Add value labels
    for i, (value, bar) in enumerate(zip(top_sources.values, bars)):
        width = bar.get_width()
        ax.text(width + (max(top_sources.values) * 0.01), bar.get_y() + bar.get_height()/2,
                f'{value:,}', ha='left', va='center', fontsize=9, weight='bold')
    
    plt.tight_layout()
    plt.savefig("top_sources.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved enhanced plot: top_sources.png")

def create_wordcloud(df):
    """Create enhanced word cloud with better styling"""
    # Clean titles and remove common stop words
    stop_words = {'the', 'and', 'of', 'in', 'to', 'a', 'for', 'with', 'on', 'by', 
                  'as', 'an', 'from', 'that', 'is', 'are', 'this', 'these', 'those'}
    
    all_titles = " ".join(df["title"].dropna().astype(str).tolist())
    
    # Remove stop words
    words = all_titles.split()
    filtered_words = [word for word in words if word.lower() not in stop_words and len(word) > 2]
    filtered_text = " ".join(filtered_words)
    
    wordcloud = WordCloud(
        width=1200, height=600, 
        background_color="white",
        colormap="plasma", 
        collocations=False,
        max_words=150,
        relative_scaling=0.5,
        min_font_size=10,
        max_font_size=120
    ).generate(filtered_text)
    
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud of COVID-19 Paper Titles", fontsize=18, weight="bold", pad=20)
    plt.tight_layout()
    plt.savefig("titles_wordcloud.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved enhanced plot: titles_wordcloud.png")

def create_publication_timeline(df):
    """Additional plot: Cumulative publications over time"""
    df_sorted = df.sort_values('publish_time')
    df_sorted['cumulative_count'] = range(1, len(df_sorted) + 1)
    
    plt.figure(figsize=(14, 7))
    plt.plot(df_sorted['publish_time'], df_sorted['cumulative_count'], 
             linewidth=3, color='#E76F51', alpha=0.8)
    
    plt.title('Cumulative COVID-19 Publications Over Time', 
              fontsize=16, weight='bold', pad=20)
    plt.xlabel('Publication Date', fontsize=12, weight='bold')
    plt.ylabel('Cumulative Number of Papers', fontsize=12, weight='bold')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('cumulative_publications.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved additional plot: cumulative_publications.png")

# Main execution function
def create_all_visualizations(df):
    """Create all visualizations with error handling"""
    try:
        print("\n" + "="*60)
        print("CREATING ENHANCED DATA VISUALIZATIONS")
        print("="*60)
        
        create_publications_by_year(df)
        create_publications_heatmap(df)
        create_top_journals(df)
        create_top_sources(df)
        create_wordcloud(df)
        create_publication_timeline(df)
        
        print("\n" + "="*60)
        print("✓ ALL VISUALIZATIONS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {str(e)}")
        raise

# Execute the visualizations
if __name__ == "__main__":
    create_all_visualizations(df)

    






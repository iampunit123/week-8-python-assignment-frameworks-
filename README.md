Perfect 👍 Here’s a **ready-to-use `README.md`** for your assignment:

---

# CORD-19 Metadata Dashboard

This project is part of the **Frameworks Assignment**. It uses the [CORD-19 dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) to explore COVID-19 research papers through data analysis and a simple **Streamlit web app**.

---

## Features

* Load and explore the **CORD-19 metadata.csv** file
* Data cleaning and sampling (avoid memory errors)
* Interactive filters:

  * Select **year range**
  * Filter by **journal**
* Visualizations:

  * Publications per year (bar chart)
  * Heatmap of publications per journal per year
  * Word cloud of paper titles
* Download filtered data as **CSV**

---

## Tools and Libraries

* Python 3.7+
* pandas (data manipulation)
* matplotlib & seaborn (visualizations)
* wordcloud (word cloud generation)
* streamlit (web application)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/iampunit123/week-8-final-assignment-python.git
cd Frameworks_Assignment
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

or (if `streamlit` is not in PATH):

```bash
python -m streamlit run app.py
```

The app will open in your browser at:

```
http://localhost:8501
```

---

## Files

* `app.py` → Streamlit app
* `metadata.csv` → dataset file (or `metadata_sample.csv` if dataset is too big)
* `requirements.txt` → dependencies list
* `README.md` → this file

---

## Expected Outputs

1. **Publications by Year** (bar chart)
2. **Heatmap** of publications per journal vs year
3. **Word Cloud** of paper titles
4. **Download Button** to export filtered results as CSV

---

## Reflection

During this project, I learned how to:

* Load and clean real-world datasets (handling missing data, sampling large files)
* Perform basic exploratory data analysis with pandas
* Create visualizations with matplotlib, seaborn, and wordcloud
* Build an interactive dashboard with Streamlit
* Document and share my work using GitHub

Challenges included dealing with the very large dataset (20+ GB). To solve this, I used only the **metadata.csv** file and sampled rows (`nrows=5000`) to make the app lightweight and fast.



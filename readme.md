# 🏙️ Tokyo Airbnb Analysis – EDA + Streamlit Dashboard

This project analyzes Airbnb listings in Tokyo, Japan, using a combination of a **Jupyter Notebook** and a **Streamlit web app**.

---

## 📁 Files Included

| File | Description |
|------|-------------|
| `main.ipynb` | Complete Exploratory Data Analysis (EDA) in notebook form — data cleaning, feature engineering, visualizations |
| `app.py` | Streamlit dashboard showcasing key insights and interactive visualizations |

---

## 📊 What’s Covered

The analysis explores:

- Distribution of listings by neighborhood
- Interactive cluster maps of listing locations
- Listing types, licenses, and availability patterns
- Identification of non-compliant listings (Minpaku law + smoke alarm)
- Review trends before and after COVID
- Top hosts and top-rated listings
- Choropleth maps for neighborhood-level pricing
- High-value listings (high ratings, low price, many reviews)


## 🖼️ Sample Screenshots


### 💎 Listings in Tokyo
![Listings Map](screenshots/Clusters.png)


### 🗺️ Average Price by Neighborhood
![Choropleth Map](screenshots/Choropleth.png)

---

### 📈 Review Trends Over the Years
![Review Trends](screenshots/Reviews.png)

---

### 🚨 Non-Compliant Listings (Minpaku + Smoke Alarm)
![Compliance Check](screenshots/Non_Compliant.png)


## 🚀 Running the Streamlit App

After placing the data:

```bash
pip install -r requirements.txt
streamlit run app.py



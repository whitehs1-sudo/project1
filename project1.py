import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load & Prepare Data
# -----------------------------
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE"
df = pd.read_csv(url)

df.rename(columns={"observation_date": "DATE"}, inplace=True)
df["DATE"] = pd.to_datetime(df["DATE"])
df["Year"] = df["DATE"].dt.year
df["Month"] = df["DATE"].dt.month_name()

# Rolling average
df["Rolling12"] = df["UNRATE"].rolling(12).mean()

# -----------------------------
# Streamlit App
# -----------------------------
st.title("U.S. Unemployment Rate Dashboard")
st.write("""
This dashboard explores long-term unemployment trends in the United States using 
monthly data from the Federal Reserve Bank of St. Louis (FRED).
""")

# -----------------------------
# Visualization 1 — Full Time Series
# -----------------------------
st.header("1. Unemployment Rate Over Time (1948–Present)")

fig1, ax1 = plt.subplots(figsize=(10,4))
ax1.plot(df["DATE"], df["UNRATE"], label="Unemployment Rate")
ax1.set_xlabel("Year")
ax1.set_ylabel("Rate (%)")
ax1.grid(True)
st.pyplot(fig1)

# -----------------------------
# Visualization 2 — Rolling 12-Month Average
# -----------------------------
st.header("2. Rolling 12-Month Average")

fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.plot(df["DATE"], df["Rolling12"], color="orange", label="12-Month Rolling Avg")
ax2.set_xlabel("Year")
ax2.set_ylabel("Rate (%)")
ax2.grid(True)
st.pyplot(fig2)

# -----------------------------
# Visualization 3 — Seasonal Pattern
# -----------------------------
st.header("3. Seasonal Pattern (Average by Month)")

monthly_avg = df.groupby("Month")["UNRATE"].mean()
monthly_avg = monthly_avg.reindex([
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
])

fig3, ax3 = plt.subplots(figsize=(10,4))
ax3.plot(monthly_avg.index, monthly_avg.values, marker="o")
ax3.set_xlabel("Month")
ax3.set_ylabel("Average Unemployment Rate (%)")
ax3.grid(True)
st.pyplot(fig3)

# -----------------------------
# Visualization 4 — Interactive Year Selector
# -----------------------------
st.header("4. Explore a Specific Year")

year_choice = st.selectbox("Select a Year:", sorted(df["Year"].unique()))

df_year = df[df["Year"] == year_choice]

fig4, ax4 = plt.subplots(figsize=(10,4))
ax4.plot(df_year["DATE"], df_year["UNRATE"], marker="o")
ax4.set_title(f"Unemployment Rate in {year_choice}")
ax4.set_xlabel("Month")
ax4.set_ylabel("Rate (%)")
ax4.grid(True)
st.pyplot(fig4)

# -----------------------------
# Data Source / Sustainability
# -----------------------------
st.header("Data Source & Sustainability")
st.write("""
**Source:** Federal Reserve Bank of St. Louis (FRED)  
**URL:** https://fred.stlouisfed.org/series/UNRATE  
**Accessed:** Today  
**License:** Public domain (U.S. Government data)

This dataset updates monthly.  
To refresh the dashboard, simply reload the CSV from the same URL.
""")

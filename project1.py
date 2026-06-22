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
st.markdown("""
## Understanding U.S. Unemployment Trends: A Visual Exploration of Labor Market Cycles

This dashboard explores long-term unemployment trends in the United States using monthly data from the Federal Reserve Bank of St. Louis (FRED). The unemployment rate measures the percentage of people actively seeking work but unable to find it. Tracking this rate helps policymakers, businesses, and citizens understand the health of the labor market and the broader economy.
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

st.markdown("""
**Interpretation:**  
Unemployment tends to rise sharply during recessions and fall during expansions. The long-term average hovers around 5–6%, but extreme events—like the 2020 pandemic—can push it far higher. Each downturn is followed by a recovery period as employment rebounds.
""")

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

st.markdown("""
**Interpretation:**  
A rolling average smooths short-term volatility and highlights sustained trends. It reveals structural changes in the labor market—such as prolonged high unemployment during the 1970s oil shocks and steady declines through the late 1990s expansion.
""")

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

st.markdown("""
**Interpretation:**  
Seasonal patterns show predictable fluctuations—employment often dips in winter and rises in summer as seasonal industries expand. These cycles remind us that not all changes in unemployment signal economic distress.
""")

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

st.markdown("""
**Interpretation:**  
Zooming into individual years helps connect national statistics to lived experiences—how quickly jobs disappeared or returned during major economic shifts such as the 2008 financial crisis or the 2020 pandemic.
""")

# -----------------------------
# Data Source / Sustainability
# -----------------------------
st.header("Data Source & Sustainability")
st.markdown("""
**Source:** Federal Reserve Bank of St. Louis (FRED)  
**Series:** UNRATE (U.S. Unemployment Rate, Seasonally Adjusted)  
**Accessed:** June 21, 2026  
**License:** Public domain (U.S. government data)  
**Refresh Instructions:** Download the latest CSV from [https://fred.stlouisfed.org/series/UNRATE](https://fred.stlouisfed.org/series/UNRATE) and replace the existing data file to keep the dashboard current.

This dataset is updated monthly by the Bureau of Labor Statistics and maintained by FRED, ensuring that the dashboard remains a living tool for ongoing analysis.
""")

st.markdown("""
### QUEST Framework Summary

**Question:** How has unemployment changed over time, and what patterns define economic cycles?  
**Understand:** Data from FRED provide monthly unemployment rates since 1948.  
**Explore:** Visualizations reveal recurring peaks during recessions and steady declines during recoveries.  
**Synthesize:** Long-term averages and seasonal patterns clarify structural labor market trends.  
**Take Action:** Understanding these cycles helps anticipate future employment shifts and guide policy responses.
""")


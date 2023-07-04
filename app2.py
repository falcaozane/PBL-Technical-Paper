import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv("Sector.csv")

# Create a sidebar where the user can select a year
selected_year = st.sidebar.selectbox("Select a year", data['Year'].dropna().unique())

# Filter the data based on the selected year
filtered_data = data[data['Year'] == selected_year]

# Select the columns for sectorwise consumption
sectors = ['Agriculture', 'Domestic', 'Commercial', 'Traction & Railways', 'Others']

# Set the colors for the sectors
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Remove rows with None values in the selected sectors
filtered_data = filtered_data.dropna(subset=sectors)

# Generate a stacked bar chart for sectorwise consumption
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(filtered_data['Industry'], filtered_data[sectors[0]], label=sectors[0], color=colors[0])
bottom = filtered_data[sectors[0]]
for i in range(1, len(sectors)):
    ax.bar(filtered_data['Industry'], filtered_data[sectors[i]], label=sectors[i], bottom=bottom, color=colors[i])
    bottom += filtered_data[sectors[i]]
ax.set_xlabel('Industry')
ax.set_ylabel('Electricity Consumed (GWh)')
ax.set_title(f'Sectorwise Electricity Consumption - {selected_year}')
ax.legend()

# Adjust spacing between subplots
plt.tight_layout()

# Display the chart
st.pyplot(fig)

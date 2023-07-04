import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data_category = pd.read_csv("data.csv")
data_sector = pd.read_csv("Sector.csv")

# Create a sidebar where the user can select a category
selected_category = st.sidebar.selectbox("Select a category", data_category['Category'].unique())

# Filter the data based on the selected category
filtered_data_category = data_category[data_category['Category'] == selected_category]

st.title("PayBill")
st.write("")

# Calculate the total Peak Demand and Peak Met for the selected category
total_peak_demand = filtered_data_category['Peak Demand'].sum()
total_peak_met = filtered_data_category['Peak Met'].sum()

# Create a dataframe for the pie chart data
pie_data = pd.DataFrame({'Category': ['Peak Demand', 'Peak Met'],
                         'Value': [total_peak_demand, total_peak_met]})

# Display the filtered data for Category
st.write(filtered_data_category)

# Generate a stacked bar chart for Peak Demand and Peak Met (Category-wise)
fig1, (ax1_1, ax1_2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# Stacked bar chart (Category-wise)
ax1_1.bar(filtered_data_category['Category'], filtered_data_category['Peak Demand'], label='Peak Demand')
ax1_1.bar(filtered_data_category['Category'], filtered_data_category['Peak Met'], label='Peak Met', bottom=filtered_data_category['Peak Demand'])
ax1_1.set_xlabel('Category')
ax1_1.set_ylabel('Value')
ax1_1.set_title('Stacked Bar Graph - Peak Demand vs Peak Met (Category-wise)')
ax1_1.legend()

# Pie chart (Category-wise)
ax1_2.pie(pie_data['Value'], labels=pie_data['Category'], autopct='%1.1f%%')
ax1_2.set_title(f'Pie Chart - Peak Demand vs Peak Met for {selected_category}')

# Adjust spacing between subplots
plt.tight_layout()



# Display the charts for Category
st.pyplot(fig1)


# Display the filtered data for Sector
st.write(data_sector)

# Generate a line chart for Yearwise Consumption of Electricity - Sectorwise
fig2, ax2 = plt.subplots(figsize=(15, 15))

sectors = ['Agriculture', 'Domestic', 'Commercial', 'Traction & Railways', 'Others']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

for sector, color in zip(sectors, colors):
    ax2.plot(data_sector['Year'], data_sector[sector], label=sector, marker='o', color=color)

ax2.set_xlabel('Year')
ax2.set_ylabel('Electricity Consumed (GWh)')
ax2.set_title('Yearwise Consumption of Electricity - Sectorwise')
ax2.legend()

# Display the chart for Sector
st.pyplot(fig2)

# Generate a bar graph for Yearwise Consumption of Electricity - Sectorwise
fig3, ax3 = plt.subplots(figsize=(15, 10))

sectors = ['Agriculture', 'Domestic', 'Commercial', 'Traction & Railways', 'Others']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

x = data_sector['Year']
bar_width = 0.15

for i, sector in enumerate(sectors):
    x_pos = [pos + i * bar_width for pos in range(len(x))]
    ax3.bar(x_pos, data_sector[sector], label=sector, color=colors[i], width=bar_width)

ax3.set_xlabel('Year')
ax3.set_ylabel('Electricity Consumed (GWh)')
ax3.set_title('Yearwise Consumption of Electricity - Sectorwise')
ax3.set_xticks(range(len(x)))
ax3.set_xticklabels(x)
ax3.legend()

# Adjust spacing between subplots
plt.tight_layout()

# Display the chart for Sector
st.pyplot(fig3)


st.write("Made by Zane Falcao and Jonathan Dabre")
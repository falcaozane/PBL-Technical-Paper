import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Load the CSV data
data_category = pd.read_csv("data.csv")
data_sector = pd.read_csv("Sector.csv")
data_consumption = pd.read_csv("consumption.csv")


st.title("PayBill")
st.divider()
st.markdown("**:violet[This is our research to make an electricity consumption calculator]**")

# Calculate the total Peak Demand and Peak Met for each category
total_peak_demand = data_category.groupby('Category')['Peak Demand'].sum()
total_peak_met = data_category.groupby('Category')['Peak Met'].sum()

# Generate a bar graph for Peak Demand and Peak Met (Category-wise)
fig, ax = plt.subplots(figsize=(12, 8))
categories = data_category['Category']
x = range(len(categories))

bar_width = 0.40
ax.bar(x, total_peak_demand, label='Peak Demand', width=bar_width)
ax.bar(x, total_peak_met, label='Peak Met', width=bar_width, bottom=total_peak_demand)

ax.set_xlabel('Month', fontsize=20,labelpad=20)
ax.set_ylabel('Power Supply(MW): Peak Demand vs Peak Met', fontsize=20,labelpad=20)
ax.set_title('Bar Graph - Peak Demand vs Peak Met (Category-wise)',fontdict={'fontsize': 20}, pad=10)
ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=35)
ax.legend()

plt.tight_layout()

# Display the bar graph
st.pyplot(fig)
st.divider()
st.write('Months | Peak-Demand(MW) | Peak-Met(MW)')
st.write(data_category)
st.divider()


# Generate a line chart for Yearwise Consumption of Electricity - Sectorwise
fig2, ax2 = plt.subplots(figsize=(18, 18))

sectors = ['Industry','Agriculture', 'Domestic', 'Commercial', 'Traction & Railways', 'Others']
colors = ['#33FFBD','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

for sector, color in zip(sectors, colors):
    ax2.plot(data_sector['Year'], data_sector[sector], label=sector, marker='^', color=color, linewidth=3)

ax2.set_xlabel('Year',fontsize=20,labelpad=20)
ax2.set_ylabel('Electricity Consumed (GWh)',fontsize=20,labelpad=20)
ax2.spines['left'].set_color('magenta')
ax2.set_title('Yearwise Consumption of Electricity - Sectorwise (line-graph)',fontdict={'fontsize': 20}, pad=10)
ax2.legend()

# Display the chart for Sector
st.pyplot(fig2)

st.divider()

# Generate a bar graph for Yearwise Consumption of Electricity - Sectorwise
fig3, ax3 = plt.subplots(figsize=(18, 18))

sectors = ['Industry','Agriculture', 'Domestic', 'Commercial', 'Traction & Railways', 'Others']
colors = ['#33FFBD','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

x = data_sector['Year']
bar_width = 0.14

for i, sector in enumerate(sectors):
    x_pos = [pos + i * bar_width for pos in range(len(x))]
    ax3.bar(x_pos, data_sector[sector], label=sector, color=colors[i], width=bar_width)

ax3.set_xlabel('Year',fontsize=20,labelpad=20)
ax3.set_ylabel('Electricity Consumed (GWh)',fontsize=20,labelpad=20)
ax3.set_title('Yearwise Consumption of Electricity - Sectorwise (bar-graph)',fontdict={'fontsize': 20}, pad=10)
ax3.set_xticks(range(len(x)))
ax3.set_xticklabels(x)
ax3.legend()

# Adjust spacing between subplots
plt.tight_layout()

# Display the chart for Sector
st.pyplot(fig3)

st.divider()

# Display the filtered data for Consumption
st.write(data_consumption)

st.divider()

# Generate a bar graph for Per Capita Consumption
fig4, ax4 = plt.subplots(figsize=(10, 6))
x = data_consumption['Years']
y = data_consumption['Per Capita Consumption']
ax4.bar(x, y, color='#E8D217')
ax4.set_xlabel('Years',fontsize=20,labelpad=20)
ax4.set_ylabel('kWh',fontsize=20,labelpad=20)
ax4.set_title('Per Capita Electricity Consumption (kWh)',fontdict={'fontsize': 20}, pad=10)
ax4.set_xticklabels(x, rotation=30)


plt.tight_layout()

# Display the chart for Per Capita Consumption
st.pyplot(fig4)

st.divider()

st.subheader("Made by Zane Falcao and Jonathan Dabre")

st.text("")
st.markdown("Credits for data : **:blue[Central Electricity Authority India & Energy Statistics India 2023]** ")
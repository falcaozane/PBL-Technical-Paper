import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Load the CSV data
data_category = pd.read_csv("data.csv")
data_sector = pd.read_csv("Sector.csv")
data_sector = data_sector.sort_values(by='Year')
data_consumption = pd.read_csv("consumption.csv")
data_predict = pd.read_csv("consumption-predict.csv")

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

ax.set_xlabel('Month', fontsize=20, labelpad=20)
ax.set_ylabel('Power Supply(MW): Peak Demand vs Peak Met', fontsize=20, labelpad=20)
ax.set_title('Bar Graph - Peak Demand vs Peak Met (Category-wise)', fontdict={'fontsize': 20}, pad=10)
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

fig2, ax2 = plt.subplots(figsize=(18, 18))

sectors = ['Industry', 'Agriculture', 'Domestic', 'Commercial', 'Traction & Railways', 'Others']
colors = ['#33FFBD', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

max_value = data_sector[sectors].values.max()  # Get the maximum value from all sectors

for sector, color in zip(sectors, colors):
    ax2.plot(data_sector['Year'], data_sector[sector], label=sector, marker='^', color=color, linewidth=3)

ax2.set_xlabel('Year', fontsize=20, labelpad=20)
ax2.set_ylabel('Electricity Consumed (GWh)', fontsize=20, labelpad=20)
ax2.spines['left'].set_color('magenta')
ax2.set_title('Yearwise Consumption of Electricity - Sectorwise (line-graph)', fontdict={'fontsize': 20}, pad=10)
ax2.legend()

# Display the chart for Sector
st.pyplot(fig2)

st.divider()

# Generate a bar graph for Yearwise Consumption of Electricity - Sectorwise
fig3, ax3 = plt.subplots(figsize=(18, 18))

sectors = ['Industry', 'Agriculture', 'Domestic', 'Commercial', 'Traction & Railways', 'Others']
colors = ['#33FFBD', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

x = data_sector['Year']
bar_width = 0.14

for i, sector in enumerate(sectors):
    x_pos = [pos + i * bar_width for pos in range(len(x))]
    ax3.bar(x_pos, data_sector[sector], label=sector, color=colors[i], width=bar_width)

ax3.set_xlabel('Year', fontsize=20, labelpad=20)
ax3.set_ylabel('Electricity Consumed (GWh)', fontsize=20, labelpad=20)
ax3.set_title('Yearwise Consumption of Electricity - Sectorwise (bar-graph)', fontdict={'fontsize': 20}, pad=10)
ax3.set_xticks(range(len(x)))
ax3.set_xticklabels(x)
ax3.legend()

# Adjust spacing between subplots
plt.tight_layout()

# Display the chart for Sector
st.pyplot(fig3)

st.divider()

st.write(data_sector)

st.divider()

# Retrieve the unique years from the Sector.csv file
years = data_sector['Year'].unique()

# Allow the user to select a specific year
selected_year = st.selectbox('Select a year', years)

# Filter the data_sector DataFrame based on the selected year
filtered_data = data_sector[data_sector['Year'] == selected_year]

# Get the values for the pie chart
values = filtered_data[['IndustryPer', 'AgriPer', 'DomPer', 'ComPer', 'TrPer', 'OtherPer']].values.flatten()

# Get the labels for the pie chart
labels = filtered_data[['Industry', 'Agriculture', 'Domestic', 'Commercial', 'Traction & Railways', 'Others']].columns

# Create a pie chart
fig4, ax4 = plt.subplots(figsize=(8, 8))
ax4.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

ax4.set_title(f'Electricity Consumption Distribution - Year {selected_year}', fontsize=16, pad=20)

# Display the pie chart
st.pyplot(fig4)

st.divider()

# Create a radar plot
fig5, ax5 = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
theta = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
values = np.concatenate((values, [values[0]]))  # Close the plot
theta = np.concatenate((theta, [theta[0]]))  # Close the plot
ax5.plot(theta, values, color='blue', marker='*')
ax5.fill(theta, values, color='blue', alpha=0.25)

ax5.set_xticks(theta[:-1])
ax5.set_xticklabels(labels, fontsize=10, fontdict={'verticalalignment': 'bottom'})
ax5.set_title(f'Electricity Consumption Distribution - Year {selected_year}', fontsize=16, pad=20)
ax5.set_ylim(0, 45)  # Set the range from 0 to 100
ax5.set_yticks(range(0, 45, 5))  # Set y-axis ticks from 0 to 100 with steps of 10

# Display the radar plot
st.pyplot(fig5)

st.divider()

# Generate a bar graph for Per Capita Consumption
fig6, ax6 = plt.subplots(figsize=(10, 6))
x = data_consumption['Years']
y = data_consumption['Per Capita Consumption']
ax6.bar(x, y, color='#E8D217')
ax6.set_xlabel('Years', fontsize=20, labelpad=20)
ax6.set_ylabel('kWh', fontsize=20, labelpad=20)
ax6.set_title('Per Capita Electricity Consumption (kWh)', fontdict={'fontsize': 20}, pad=10)
ax6.set_xticklabels(x, rotation=30)

plt.tight_layout()

# Display the chart for Per Capita Consumption
st.pyplot(fig6)

st.divider()

# Display the filtered data for Consumption
st.write(data_consumption)

# Extract the features (Years) and target variable (Per Capita Consumption)
X = data_predict['Years'].values.reshape(-1, 1)
y = data_predict['Per Capita Consumption'].values

# Train the linear regression model
regression_model = LinearRegression()
regression_model.fit(X, y)

# Years to predict
years_to_predict = ['2022-23', '2023-24']

# Predict the Per Capita Consumption for the given years
X_pred = np.array([int(year.split('-')[0]) for year in years_to_predict]).reshape(-1, 1)
y_pred = regression_model.predict(X_pred)

# Create a DataFrame to display the predictions
predictions_df = pd.DataFrame({'Years': years_to_predict, 'Per Capita Consumption': y_pred})

# Display the predictions
st.subheader("Per Capita Consumption Predictions (kWh)")
st.write("Calculated by performing linear regression (Skit-Learn) on existing values")
st.write(predictions_df)

st.divider()
st.subheader("Made by: Zane Falcao & Jonathan Dabre")

st.text("")
st.markdown("Credits for data: **:blue[Central Electricity Authority India & Energy Statistics India 2023]** ")

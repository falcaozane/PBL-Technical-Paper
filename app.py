import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Load the CSV data
data_category = pd.read_csv("data.csv")
data_sector = pd.read_csv("Sector.csv")
data_consumption = pd.read_csv("consumption.csv")
data_predict = pd.read_csv("consumption-predict.csv")

st.title("PayBill")
st.divider()
st.markdown("**:violet[This is our research to make an electricity consumption calculator]**")

import numpy as np

# Calculate the total Peak Demand and Peak Met for each category
total_peak_demand = data_category.groupby('Category')['Peak Demand'].sum()
total_peak_met = data_category.groupby('Category')['Peak Met'].sum()

# Generate a dual-axis line graph for Peak Demand and Peak Met (Category-wise)
fig, ax1 = plt.subplots(figsize=(12, 8))
categories = data_category['Category']
x = np.arange(len(categories))

# Plot the Peak Demand as a line plot
ax1.plot(x, total_peak_demand, marker='v', label='Peak Demand')
ax1.set_xlabel('Months', fontsize=20, labelpad=20)
ax1.set_ylabel('Peak Demand', fontsize=20, labelpad=20)
ax1.tick_params(axis='y')
ax1.legend(loc='upper left')

# Create a second y-axis
ax2 = ax1.twinx()

# Plot the Peak Met as a line plot
ax2.plot(x, total_peak_met, marker='^', color='tab:orange', label='Peak Met')
ax2.set_ylabel('Peak Met', fontsize=20, labelpad=20)
ax2.tick_params(axis='y')
ax2.legend(loc='upper right')

# Set the x-axis ticks and labels
ax1.set_xticks(x)
ax1.set_xticklabels(categories, rotation=35)

# Set the title
ax1.set_title('Dual-Axis Line Graph - Peak Demand vs Peak Met (Month-wise)', fontdict={'fontsize': 20}, pad=20)
ax1.legend(loc='lower left')
ax2.legend(loc='lower right')
plt.tight_layout()

# Display the line graph
st.pyplot(fig)
st.markdown("**:orange[Dual-Axis Line Graph - Peak Demand vs Peak Met (Month-wise): ]**")
st.markdown("The dual-axis line graph compares the peak demand and peak met values for every month. It allows for a direct comparison of the two variables on separate y-axes. The graph shows the variation between peak demand and peak met across every month,indicating the effectiveness of meeting the peak power demand.By analyzing this graph, it becomes evident which categories consistently meet or exceed peak demand and which categories may need further attention to ensure sufficient power supply during peak periods.")
st.markdown("**:green[After visualizing the data we can conclude that the demand for electricity was only met in the months of Feb, May, August & November.]**")

st.divider()
st.write('Months | Peak-Demand(MW) | Peak-Met(MW)')
st.write(data_category)
st.divider()

# Extract the features (Months) and target variable (Peak Demand)
X = data_category['Month.no'].values.reshape(-1, 1)
y = data_category['Peak Demand']

# Train the linear regression model
regression_model = LinearRegression()
regression_model.fit(X, y)

# Months to predict
months_to_predict = ['Apr-23', 'May-23', 'Jun-23', 'Jul-23', 'Aug-23', 'Sep-23', 'Oct-23', 'Nov-23', 'Dec-23', 'Jan-24']

# Predict the Peak Demand for the given months
X_pred = np.array([pd.to_datetime(month, format='%b-%y').month for month in months_to_predict]).reshape(-1, 1)
y_pred = regression_model.predict(X_pred)

# Create a DataFrame to display the predictions
predictions_df = pd.DataFrame({'Months': months_to_predict, 'Peak Demand': y_pred})

# Display the predictions
st.subheader("Peak Demand Predictions (in MW) from April 2023 to January 2024")
st.markdown("**:orange[Calculated by performing Linear regression(Scikit-Learn) on existing values]**")
st.write(predictions_df)



st.divider()

# Add a select box to choose a sector
selected_sector = st.selectbox('Select a sector', ['Industry', 'Agriculture', 'Domestic', 'Commercial', 'Traction & Railways', 'Others'])

# Sort the data by year and selected sector
data_sector_sorted = data_sector.sort_values(by=['Years', selected_sector])

# Generate a line graph for Yearwise Consumption of Electricity - Sectorwise
fig2, ax2 = plt.subplots(figsize=(8, 5))
x = data_sector_sorted['Years']
y = data_sector_sorted[selected_sector]
ax2.plot(x, y, label=selected_sector, marker='^', color='blue', linewidth=2)

ax2.set_xlabel('Year', fontsize=20, labelpad=20)
ax2.set_ylabel('Electricity Consumed (GWh)', fontsize=20, labelpad=20)
ax2.spines['left'].set_color('magenta')
ax2.spines['bottom'].set_color('magenta')
ax2.set_xticklabels(x, rotation=75)
ax2.set_title(f'Yearwise Consumption of Electricity - {selected_sector}', fontdict={'fontsize': 20}, pad=10)
ax2.legend()

# Display the chart for the selected sector
st.pyplot(fig2)

st.divider()

# Generate a bar graph for Yearwise Consumption of Electricity - Sectorwise
fig3, ax3 = plt.subplots(figsize=(8, 6))
x = data_sector_sorted['Years']
y = data_sector_sorted[selected_sector]

bar_width = 0.5

ax3.bar(x, y, label=selected_sector, color='magenta', width=bar_width)

ax3.set_xlabel('Year', fontsize=20, labelpad=20)
ax3.set_ylabel('Electricity Consumed (GWh)', fontsize=20, labelpad=20)
ax3.set_title(f'Yearwise Consumption of Electricity - {selected_sector}', fontdict={'fontsize': 20}, pad=10)
ax3.set_xticklabels(x, rotation=80)
ax3.legend()

# Adjust spacing between subplots
plt.tight_layout()

# Display the chart for the selected sector
st.pyplot(fig3)



st.divider()

st.write(data_sector)

st.markdown("**:orange[Sector wise distribution of electricity consumption using line and bar graph over the years ]**")

st.divider()

# Retrieve the unique years from the Sector.csv file
years = data_sector['Years'].unique()

# Allow the user to select a specific year
original_title = '<p style="font-family:Sans-serif; color:purple; font-size: 30px;">Select a year</p>'
st.markdown(original_title, unsafe_allow_html=True)
selected_year = st.selectbox('Years', years)

# Filter the data_sector DataFrame based on the selected year
filtered_data = data_sector[data_sector['Years'] == selected_year]

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
ax5.plot(theta, values, color='orange', marker='*')
ax5.fill(theta, values, color='orange', alpha=0.35)

ax5.set_xticks(theta[:-1])
ax5.set_xticklabels(labels, fontsize=10, fontdict={'verticalalignment': 'bottom'})
ax5.set_title(f'Electricity Consumption Distribution - Year {selected_year}', fontsize=16, pad=20)
ax5.set_ylim(0, 45)  # Set the range from 0 to 100
ax5.set_yticks(range(0, 45, 5))  # Set y-axis ticks from 0 to 100 with steps of 10

# Display the radar plot
st.pyplot(fig5)

st.markdown("**:orange[Sector wise percentage distribution of electricity consumption using pie and radar plot over the years ]**")
st.markdown("From the graphs, we can see that the Industry sector has the highest consumption ( always greater than 40%). Automation and electrification in the Agriculture sector have seen a steep rise in electricity consumption.")
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
ax6.legend()

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
st.markdown("**:orange[Calculated by performing linear regression (Scikit-Learn) on existing values]**")
st.write(predictions_df)
st.markdown("**:orange[Conclusion for Per Capita Electricity Consumption Graph: ]**")
st.markdown("The Per Capita Electricity Consumption graph showcases the average electricity consumption(in MW) every year over a specific time period. It provides insights into the electricity consumption patterns of a population and can be indicative of energy usage, lifestyle, and economic factors. From the graph, it can be observed that the per capita electricity consumption has experienced a gradual increase over time. This may indicate a rise in living standards, economic growth, and increased access to electrical appliances and technologies. The graph also reveals fluctuations and variations in consumption, which could be attributed to seasonal variations, changes in energy policies, or shifts in population demographics. In the year 2020-21 the consumption decreased because of Covid-19. Understanding per capita electricity consumption is essential for energy planning, policy-making, and sustainability efforts. It helps identify areas of high or low energy consumption, allowing policymakers and energy providers to develop targeted strategies for energy conservation, efficiency, and renewable energy adoption. Additionally, it can assist in evaluating the impact of energy-saving initiatives and promoting awareness among individuals and communities about responsible electricity usage. Overall, the Per Capita Electricity Consumption graph provides valuable insights into the trends and patterns of electricity consumption per person. It serves as a tool for policymakers, energy planners, and individuals to make informed decisions regarding energy conservation, efficiency measures, and the transition to cleaner and sustainable energy sources.**:green[ With more evolution and development the consumption rate is set to increase.]**")

st.divider()
st.subheader("Made by: Zane Falcao & Jonathan Dabre")

st.text("")
st.markdown("Credits for data: **:blue[Central Electricity Authority India & Energy Statistics India 2023]** ")

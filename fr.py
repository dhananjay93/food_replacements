import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Sample data for two groups of food items
data_group1 = {
    'Food': ['Poha', 'Paneer', 'Rice', 'A', 'B', 'C', 'D'],
    'Weight': [100, 50, 100, 40, 50, 60, 70],
    'Group': ['Carbs'] * 7
}

data_group2 = {
    'Food': ['E', 'F', 'G', 'Z', 'H', 'I', 'J'],
    'Weight': [100, 50, 100, 40, 50, 60, 70],
    'Group': ['Protein'] * 7
}

df_group1 = pd.DataFrame(data_group1)
df_group2 = pd.DataFrame(data_group2)

# Combine both dataframes
df_combined = pd.concat([df_group1, df_group2], ignore_index=True)

# Streamlit app
st.title("Food Weight Visualization Streamlit")

# Dropdown to select a food item
selected_food = st.selectbox("Select a food item", df_combined['Food'])

# Slider to adjust the amount
selected_amount = st.slider("Select amount", min_value=0, max_value=200, step=10, value=100)

# Filter data based on selected food
filtered_df = df_combined[df_combined['Food'] == selected_food]
selected_food_group = filtered_df['Group'].iloc[0]

# Calculate adjusted weights proportionately based on slider value
original_selected_weight = filtered_df['Weight'].iloc[0]
proportion = selected_amount / original_selected_weight
adjusted_weights = filtered_df['Weight'] * proportion

# Display the adjusted weights in a table
st.write(f"Food Weights ({selected_food_group}) excluding {selected_food}")
table_data = {'Food': filtered_df['Food'], 'Weight': adjusted_weights}
st.write(pd.DataFrame(table_data))

# Optionally, display the weights in a Plotly table
table_fig = go.Figure(data=[go.Table(
    header=dict(values=['Food', 'Weight'],
                fill_color='lightblue',
                align='left'),
    cells=dict(values=[filtered_df['Food'], adjusted_weights],
               fill_color='white',
               align='left'))
])

st.plotly_chart(table_fig)

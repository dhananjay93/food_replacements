import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Sample data for three groups of food items
data_group1 = {
    'Food': [
        "Rice", "Wheat flour (if you can digest it well)", "Rice flour", "Any dal/legume",
        "Millet flour (Ragi/Bajra/Jowar etc.)", "Oats (preferably rolled or steel cut)",
        "Rice cake (unsweetened)", "Besan or thalipeeth flour", "Gluten-free pasta (easier to digest)",
        "Gluten-free noodles (easier to digest)", "Quinoa", "Couscous", "Poha", "Rawa (semolina)",
        "Bread (preferably multigrain or sourdough)", "Dosa / idli batter", "Potato/sweet potato"
    ],
    'Weight': [
        100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 
        100, 100, 100, 100, 150, 200, 400
    ],
    'Protein': [0] * 17,
    'Carbs': [0] * 17,
    'Fats': [0] * 17,
    'Total Calories': [0] * 17,
    'Group': ['Carbs'] * 17
}

data_group2 = {
    'Food': [
        "Chicken meat", "Fish", "Prawn/crab meat", "Turkey",
        "Whey protein", "Tofu", "Low-fat paneer", "Paneer (lower protein)"
    ],
    'Weight': [100, 100, 100, 100, 30, 100, 100, 50],
    'Protein': [0] * 8,
    'Carbs': [0] * 8,
    'Fats': [0] * 8,
    'Total Calories': [0] * 8,
    'Group': ['Protein Group 1'] * 8
}

data_group3 = {
    'Food': ["Paneer", "Red meat or 4 eggs", "Cheese"],
    'Weight': [100, 100, 100],
    'Protein': [0] * 3,
    'Carbs': [0] * 3,
    'Fats': [0] * 3,
    'Total Calories': [0] * 3,
    'Group': ['Protein Group 2'] * 3
}

# Create DataFrames
df_group1 = pd.DataFrame(data_group1)
df_group2 = pd.DataFrame(data_group2)
df_group3 = pd.DataFrame(data_group3)

# Combine all dataframes
df_combined = pd.concat([df_group1, df_group2, df_group3], ignore_index=True)

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Food Replacement Options", style={'text-align': 'center', 'color': '#333333'}),
    html.Div([
        html.Label("Select a food item:", style={'margin-right': '10px'}),
        dcc.Dropdown(
            id='food-dropdown',
            options=[{'label': food, 'value': food} for food in df_combined['Food']],
            placeholder="Select a food item",
            style={'width': '50%', 'margin-right': '10px'}
        ),
        html.Label("Adjust amount (grams):", style={'margin-right': '10px'}),
        dcc.Slider(
            id='amount-slider',
            min=0,
            max=200,
            step=10,
            value=100,
            marks={i: str(i) for i in range(0, 201, 20)}  # Display marks every 20 units
        ),
    ], style={'width': '80%', 'margin': 'auto', 'text-align': 'center', 'padding': '20px'}),
    
    html.Div(id='table-container', style={'padding': '20px', 'text-align': 'center'})
])

# Define callback to update table based on selected food item and slider value
@app.callback(
    Output('table-container', 'children'),
    [Input('food-dropdown', 'value'),
     Input('amount-slider', 'value')]
)
def update_table(selected_food, selected_amount):
    if selected_food is None:
        return html.Div("Please select a food item.", style={'color': 'red', 'font-size': '18px', 'text-align': 'center'})

    selected_food_group = df_combined.loc[df_combined['Food'] == selected_food, 'Group'].values[0]
    filtered_df = df_combined[df_combined['Group'] == selected_food_group]

    # Calculate adjusted weights proportionately based on slider value
    original_weights = filtered_df['Weight']
    original_selected_weight = df_combined.loc[df_combined['Food'] == selected_food, 'Weight'].values[0]
    
    if original_selected_weight == 0:
        adjusted_weights = original_weights  # Avoid division by zero
    else:
        proportion = selected_amount / original_selected_weight
        adjusted_weights = original_weights * proportion
    
    # Update Total Calories based on adjusted weights (for display purposes)
    filtered_df['Total Calories'] = adjusted_weights * 0  # Assuming 4 calories per gram (generic)

    # Filter out the selected food item from displaying in the table
    filtered_table_data = [(food, weight, protein, carbs, fats, calories) for food, weight, protein, carbs, fats, calories in 
                           zip(filtered_df['Food'], adjusted_weights, filtered_df['Protein'], 
                               filtered_df['Carbs'], filtered_df['Fats'], filtered_df['Total Calories']) if food != selected_food]
    
    # Create a Plotly table
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=['Food', 'Weight (grams)', 'Protein', 'Carbs', 'Fats', 'Total Calories'],
                    fill_color='#f2f2f2',
                    align='left'),
        cells=dict(values=[list(col) for col in zip(*filtered_table_data)],  # Use the filtered data here
                   fill_color='white',
                   align='left'))
    ])
    
    # Update table layout
    table_fig.update_layout(
        title=f"Alternatives for {selected_amount}gm of {selected_food}",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family="Arial, sans-serif", size=12),
        width=800, height=500  # Adjust width and height as needed
    )
    
    # Convert Plotly figure to HTML and return
    table_html = dcc.Graph(figure=table_fig)
    return table_html

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

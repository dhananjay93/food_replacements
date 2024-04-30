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
    'Group': ['Carbs'] * 17
}

data_group2 = {
    'Food': [
        "Chicken meat", "Fish", "Prawn/crab meat", "Turkey",
        "Whey protein", "Tofu", "Low-fat paneer", "Paneer (lower protein)"
    ],
    'Weight': [100, 100, 100, 100, 30, 100, 100, 50],
    'Group': ['Protein Group 1'] * 8
}

data_group3 = {
    'Food': ["Paneer", "Red meat or 4 eggs", "Cheese"],
    'Weight': [100, 100, 100],
    'Group': ['Protein Group 2'] * 3
}

df_group1 = pd.DataFrame(data_group1)
df_group2 = pd.DataFrame(data_group2)
df_group3 = pd.DataFrame(data_group3)

# Combine all dataframes
df_combined = pd.concat([df_group1, df_group2, df_group3], ignore_index=True)

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define colors and styles
colors = {
    'background': '#f9f9f9',
    'text': '#333333',
    'accent': '#007BFF'
}

# Define the layout of the app
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    html.H1("Food Weight Visualization", style={'textAlign': 'center', 'color': colors['text']}),

    html.Div([
        html.Label("Select a food item:", style={'margin-right': '10px', 'color': colors['text']}),
        dcc.Dropdown(
            id='food-dropdown',
            options=[{'label': food, 'value': food} for food in df_combined['Food']],
            placeholder="Select a food item",
            style={'width': '50%', 'margin-right': '10px'}
        ),
        html.Label("Adjust amount (grams):", style={'margin-right': '10px', 'color': colors['text']}),
        html.Div(
            dcc.Slider(
                id='amount-slider',
                min=0,
                max=200,
                step=10,
                value=100,
                marks={i: str(i) for i in range(0, 201, 20)},  # Display marks every 20 units
            ),
            style={'width': '70%', 'margin-bottom': '20px'}
        ),
    ], style={'width': '80%', 'margin': 'auto', 'textAlign': 'center'}),

    html.Div(id='table-container')
])

# Define callback to update table based on selected food item and slider value
@app.callback(
    Output('table-container', 'children'),
    [Input('food-dropdown', 'value'),
     Input('amount-slider', 'value')]
)
def update_table(selected_food, selected_amount):
    if selected_food is None:
        return html.Div("Please select a food item.", style={'color': 'red', 'fontSize': '18px', 'textAlign': 'center'})

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
    
    # Create a Plotly table
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=['Food', 'Weight (grams)'],
                    fill_color=colors['accent'],
                    font=dict(color='white', size=14),
                    align='left'),
        cells=dict(values=[filtered_df['Food'], adjusted_weights],
                   fill_color='white',
                   font=dict(color=colors['text'], size=14),
                   align='left'))
    ])
    
    # Update table layout
    table_fig.update_layout(
        title=f"Alternatives for {selected_food}",
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family="Arial, sans-serif", size=14),
        width=600, height=300
    )
    
    # Convert Plotly figure to HTML and return
    table_html = dcc.Graph(figure=table_fig)
    return table_html

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

python
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the dataset
data_path = 'Yearly_Water_Consumption_Data_2021_2025.csv'
data = pd.read_csv(data_path)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Regional Water Consumption Dashboard (2021-2025)"),
    html.Label("Select Region:"),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in data['Region'].unique()],
        value=data['Region'].unique()[0],
        clearable=False
    ),
    html.Label("Select Year:"),
    dcc.Slider(
        id='year-slider',
        min=data['Year'].min(),
        max=data['Year'].max(),
        marks={year: str(year) for year in range(data['Year'].min(), data['Year'].max() + 1)},
        value=data['Year'].min(),
        step=1
    ),
    dcc.Graph(id='water-consumption-graph')
])

@app.callback(
    Output('water-consumption-graph', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_region, selected_year):
    filtered_data = data[(data['Region'] == selected_region) & (data['Year'] == selected_year)]
    figure = px.bar(filtered_data, x='Region', y='Water_Consumption', title=f'Water Consumption in {selected_region} for {selected_year}')
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)

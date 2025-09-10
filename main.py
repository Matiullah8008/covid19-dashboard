import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output

# -----------------------------
# Load and prepare data
# -----------------------------
df = pd.read_csv("owid_covid_cleaned.csv")
df['date'] = pd.to_datetime(df['date'])

# Keep only countries
df = df[df['iso_code'].str.len() == 3]

# Fill missing
df['new_cases'] = df['new_cases'].fillna(0)
df['new_deaths'] = df['new_deaths'].fillna(0)
df['people_vaccinated_per_hundred'] = df['people_vaccinated_per_hundred'].fillna(0)
df['total_vaccinations'] = df['total_vaccinations'].fillna(0)
df['total_cases_per_million'] = df['total_cases_per_million'].fillna(0)
df['total_deaths_per_million'] = df['total_deaths_per_million'].fillna(0)

# -----------------------------
# Initialize Dash App
# -----------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "COVID-19 Dashboard"

# -----------------------------
# Layout
# -----------------------------
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("COVID-19 Interactive Dashboard",
                    className="text-center text-primary mb-4"),
            html.P("Explore cases, deaths, vaccinations, and policy responses across the world.",
                   className="text-center text-secondary"),
        ])
    ]),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Total Cases"), html.H5(id='total-cases-kpi')])), width=4),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Total Deaths"), html.H5(id='total-deaths-kpi')])), width=4),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Total Vaccinations"), html.H5(id='total-vaccinations-kpi')])), width=4),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Filters", className="card-title"),
                    html.Label("Select Continent:"),
                    dcc.Dropdown(
                        id='continent-dropdown',
                        options=[{'label': c, 'value': c} for c in sorted(df['continent'].unique())],
                        value='Asia',
                        multi=False
                    ),
                    html.Br(),
                    html.Label("Select Country:"),
                    dcc.Dropdown(
                        id='country-dropdown',
                        multi=False
                    ),
                    html.Br(),
                    html.Label("Select Metric:"),
                    dcc.Dropdown(
                        id='metric-dropdown',
                        options=[
                            {'label': 'Total Cases', 'value': 'total_cases'},
                            {'label': 'Total Deaths', 'value': 'total_deaths'},
                            {'label': 'Total Vaccinations', 'value': 'total_vaccinations'},
                            {'label': 'People Vaccinated (%)', 'value': 'people_vaccinated_per_hundred'}
                        ],
                        value='total_cases',
                        multi=False
                    ),
                    html.Br(),
                    html.Label("Select Date Range:"),
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date=df['date'].min(),
                        end_date=df['date'].max(),
                        display_format='YYYY-MM-DD'
                    ),
                    html.Br(),
                    html.Br(),
                    html.Label("Select Data Aggregation:"),
                    dcc.RadioItems(
                        id='aggregation-toggle',
                        options=[
                            {'label': 'Daily', 'value': 'D'},
                            {'label': 'Weekly', 'value': 'W'},
                            {'label': 'Monthly', 'value': 'M'}
                        ],
                        value='D',
                        labelStyle={'display': 'inline-block'}
                    )
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id='timeseries-chart')], width=12)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id='world-map')], width=6),
                dbc.Col([dcc.Graph(id='bar-chart')], width=6)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id='scatter-plot')], width=12)
            ])
        ], width=9)
    ])
], fluid=True)

# -----------------------------
# Callbacks
# -----------------------------

# Update KPIs
@app.callback(
    [Output('total-cases-kpi', 'children'),
     Output('total-deaths-kpi', 'children'),
     Output('total-vaccinations-kpi', 'children')],
    [Input('country-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_kpis(country, start_date, end_date):
    if country:
        dff = df[(df['location'] == country) & (df['date'] >= start_date) & (df['date'] <= end_date)]
    else:
        dff = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    total_cases = dff['total_cases'].max()
    total_deaths = dff['total_deaths'].max()
    total_vaccinations = dff['total_vaccinations'].max()
    
    return f"{total_cases:,.0f}", f"{total_deaths:,.0f}", f"{total_vaccinations:,.0f}"


# Update country dropdown based on continent
@app.callback(
    Output('country-dropdown', 'options'),
    Input('continent-dropdown', 'value')
)
def update_country_dropdown(continent):
    if continent:
        countries = df[df['continent'] == continent]['location'].unique()
        return [{'label': c, 'value': c} for c in sorted(countries)]
    else:
        countries = df['location'].unique()
        return [{'label': c, 'value': c} for c in sorted(countries)]

@app.callback(
    Output('country-dropdown', 'value'),
    Input('country-dropdown', 'options')
)
def set_country_value(available_options):
    if available_options:
        return available_options[0]['value']
    return None

# Time-series
@app.callback(
    Output('timeseries-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('metric-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('aggregation-toggle', 'value')]
)
def update_timeseries(country, metric, start_date, end_date, aggregation):
    if not country:
        return px.line(title="Please select a country", template="plotly_dark")
    dff = df[(df['location'] == country) & (df['date'] >= start_date) & (df['date'] <= end_date)]
    if aggregation != 'D':
        dff = dff.resample(aggregation, on='date').sum().reset_index()
    dff['rolling_avg'] = dff[metric].rolling(7).mean()
    fig = px.line(dff, x='date', y=metric,
                  title=f"{metric.replace('_',' ').title()} in {country}", template="plotly_dark")
    fig.add_scatter(x=dff['date'], y=dff['rolling_avg'], mode='lines', name='7-Day Rolling Average')
    fig.update_layout(transition_duration=500)
    return fig

# World map
@app.callback(
    Output('world-map', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('continent-dropdown', 'value')]
)
def update_map(metric, continent):
    dff = df.copy()
    dff['date'] = dff['date'].dt.strftime('%Y-%m-%d')
    if continent:
        dff = dff[dff['continent'] == continent]
    fig = px.choropleth(dff, locations="iso_code", color=metric,
                        hover_name="location",
                        color_continuous_scale="Reds",
                        animation_frame="date",
                        animation_group="location",
                        title=f"Global {metric.replace('_',' ').title()}", template="plotly_dark")
    return fig

# Bar chart (Top 10 countries)
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('continent-dropdown', 'value')]
)
def update_bar(metric, continent):
    latest_date = df['date'].max()
    latest = df[df['date'] == latest_date]
    if continent:
        latest = latest[latest['continent'] == continent]
    top10 = latest.nlargest(10, metric)
    fig = px.bar(top10, x='location', y=metric,
                 title=f"Top 10 Countries by {metric.replace('_',' ').title()} (Latest Date)", template="plotly_dark")
    return fig

# Scatter plot (Vaccination vs Deaths)
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('continent-dropdown', 'value')]
)
def update_scatter(metric, continent):
    latest_date = df['date'].max()
    latest = df[df['date'] == latest_date]
    if continent:
        latest = latest[latest['continent'] == continent]
    fig = px.scatter(latest, x="people_vaccinated_per_hundred",
                     y="total_deaths_per_million",
                     size="population",
                     color="continent",
                     hover_name="location",
                     title="Vaccination vs Deaths per Million", template="plotly_dark")
    return fig

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.data as pldata

# Load the gapminder dataset
df = pldata.gapminder()

# Create a Series of unique countries (remove duplicates)
countries = df['country'].unique()
countries = sorted(countries)  

app = dash.Dash(__name__)
server = app.server  # <-- This is the line you need to add

app.layout = html.Div([
    html.H1('GDP Per Capita Dashboard', style={'textAlign': 'center'}),
    
    html.Div([
        html.Label('Select Country:'),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in countries],
            value='Canada',
            style={'width': '50%'}
        )
    ], style={'margin': '20px'}),
    
    dcc.Graph(id='gdp-growth')
])


@app.callback(
    Output('gdp-growth', 'figure'),
    Input('country-dropdown', 'value')
)
def update_graph(selected_country):
    filtered_df = df[df['country'] == selected_country]
    
    fig = px.line(
        filtered_df,
        x='year',
        y='gdpPercap',
        title=f'GDP Per Capita Over Time - {selected_country}',
        labels={
            'year': 'Year',
            'gdpPercap': 'GDP Per Capita (USD)',
            'country': 'Country'
        }
    )
    

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='GDP Per Capita (USD)',
        showlegend=False
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)

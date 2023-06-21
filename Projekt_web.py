
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

#Nahrání dataframu
df = pd.read_excel("Ideologie.xlsx")


# Převedení 'market_indices' na správný datový typ
df['market_indices'] = pd.to_numeric(df['market_indices'], errors='coerce')

# Nahrazení Na hodnotou 0 protože pandas s tím má jinak problémy
df['market_indices'] = df['market_indices'].fillna(0)

# Seznam všech zemí pro výběr v menu
countries = df['country_name'].unique()

#Začíná se pracovat v rámci aplikace
app = dash.Dash(__name__)

#Jak bude vypadat menu a aplikace
app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown', #ID pro menu zemí
        options=[{'label': i, 'value': i} for i in countries],
        value='Germany'  # Výchozí hodnota
    ),
    dcc.Graph(id='my-graph') #Využíváme příkaz k zobrazení grafu v rámci Dash aplikace a přiřazujeme ID protože Dash při manipulaci potřebuje unikátní ID pro komponenty.
], style={'width': '500'})

#Callback při změně vybrané změně v tom menu
@app.callback(
    Output(component_id='my-graph', component_property='figure'), #Voláme znovu to ID v rámci dcc.graph, které jsem navolil.
    [Input(component_id='country-dropdown', component_property='value')] #Vpodstatě to stejné ale pro ID menu.
)
def update_graph(selected_dropdown_value):
    dff = df[df['country_name'] == selected_dropdown_value] #Vytvoří se nový dataframe dff místo df aby se nepoškodily původní data pro jistotu.. ale není to úplně nutný
    dff['rounded_market_indices'] = round(dff['market_indices'], 1)
    return {
        'data': [
            #Je definováno jak má vypadat ten graf univerzálně pro všechny možnosti. Neliší se moc od R.
            go.Scatter(
                x=dff['year'],
                y=dff['market_indices'],
                mode='lines+markers',
                hoverinfo='text',
                hovertext=dff['year'].astype(str) + ', ' + dff['rounded_market_indices'].astype(str)
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Rok'},
            yaxis={'title': '% změna hodnoty akciového indexu'},
        )
    }
#Spouští se už nyní Dash server/aplikace
if __name__ == '__main__':
    app.run_server(debug=True)
import dash
from dash import dcc, html
import plotly.graph_objs as go

def determinar_piso(salario, salario_pisos):
    for i in range(len(salario_pisos) - 1):
        if salario_pisos[i] <= salario < salario_pisos[i + 1]: #verifica si el salario cae entre dos valores consecutivos
            return i + 1
    return len(salario_pisos)

def gradiente_color(nivel, pisos):
    red = max(0, min(255, int((pisos - nivel) / (pisos - 1) * 255)))
    green = max(0, min(255, int((nivel - 1) / (pisos - 1) * 255)))
    return f'rgb({red}, {green}, 0)'
def create_dash_app(flask_app, piramide, clases_pisos):
    dash_app = dash.Dash(
        server=flask_app,
        routes_pathname_prefix='/dash/',
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )

    # Layout de Dash
    dash_app.layout = html.Div([
        html.H1('Buscate en la Pirámide Social Argentina'),
        dcc.Input(id='salario-input', type='number', value=0, step=10000),
        html.Button('Calcular', id='submit-val', n_clicks=0),
        dcc.Graph(id='piramide-grafico'),
        html.Div(id='output-container')
    ])

    # Callback de Dash
    @dash_app.callback(
        [dash.dependencies.Output('piramide-grafico', 'figure'),
         dash.dependencies.Output('output-container', 'children')],
        [dash.dependencies.Input('submit-val', 'n_clicks')],
        [dash.dependencies.State('salario-input', 'value')]
    )
    def update_figure(n_clicks, selected_salario):
        anchos_por_piso = [10, 8, 6, 4, 2]
        estrato_usuario = determinar_piso(selected_salario, piramide)
        figuras = []
        
        # Dibujar los pisos de la pirámide
        for i in range(len(clases_pisos)):
            figuras.append(go.Scatter(
                x=[-anchos_por_piso[i]/2, anchos_por_piso[i]/2],
                y=[i, i],
                mode='lines',
                line=dict(width=0, color=str(gradiente_color(i, len(piramide)))),
                fill='tonexty',
                showlegend=False
            ))

        # Agregar el marcador para la ubicación del usuario
        figuras.append(go.Scatter(
            x=[0],
            y=[estrato_usuario - 1],
            mode='markers+text',
            marker=dict(size=15, color='purple'),
            text=['Tu ubicación en la pirámide'],  # Personaliza el texto
            textposition="top center",
            name='Acá estás'  # Personaliza el nombre del marcador
        ))

        layout = go.Layout(
            xaxis=dict(visible=False),
            yaxis=dict(
                tickvals=list(range(len(clases_pisos))),  # Incluye el nivel superior
                ticktext=[f"{clases_pisos[i]}, mínimo de ${piramide[i]}" for i in range(len(clases_pisos))] ,
                range=[-0.5, len(clases_pisos)],  
            ),
            margin=dict(l=50, r=50, t=50, b=50),
            height=400,
        )

        figure = go.Figure(data=figuras, layout=layout)
        salida = f"Con un salario de ${selected_salario}, eres {clases_pisos[estrato_usuario - 1]}"
        return figure, salida

    return dash_app

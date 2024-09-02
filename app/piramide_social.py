import dash
from dash import dcc, html
import plotly.graph_objs as go

def gradiente_color(nivel, pisos):
    red = max(0, min(255, int((pisos - nivel) / (pisos - 1) * 255)))
    green = max(0, min(255, int((nivel - 1) / (pisos - 1) * 255)))
    return f'rgb({red}, {green}, 0)'

def armar_piramide(adultos,ninos,alquiler,cba,cbt):  
    return [alquiler,  # Base de la pirámide
            alquiler + (cba * (adultos + ninos * 0.68)),
            alquiler + (cbt * (adultos  + ninos * 0.68)),
            alquiler + (2.5 * cbt * (adultos + ninos * 0.68)), 
            alquiler + (3.5 * cbt * (adultos + ninos * 0.68)),
            alquiler + (4.5 * cbt * (adultos + ninos * 0.68))        ]

def get_image_for_position(y_usuario):
    if y_usuario < 1:
        return '/static/img/bart.png'
    elif y_usuario < 2:
        return '/static/img/perrito.jpeg'
    elif y_usuario < 3:
        return '/static/img/elsa.jpeg'
    elif y_usuario < 4:
        return '/static/img/fry.jpeg'
    elif y_usuario < 5:
        return '/static/img/platudo.png'
    elif y_usuario < 6:
        return '/static/img/ricky.jpg'

def create_dash_app(flask_app, clases_pisos, cba, cbt):
    dash_app = dash.Dash(
        server=flask_app,
        routes_pathname_prefix='/dash/',
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )
    
    # Layout de Dash
    dash_app.layout = html.Div([
    html.Div([
        html.Label('Salario en múltiplo de 10000    :'),
        dcc.Input(id='salario-input', type='number', value=0, step=10000),
    ], style={'display': 'inline-block'}),  # Espaciado entre los elementos
    html.Div([
        html.Label('Cantidad de Adultos:'),
        dcc.Input(id='adultos-input', type='number', value=1, step=1)
    ], style={'display': 'inline-block'}),
    html.Div([
        html.Label('Cantidad de Niños:'),
        dcc.Input(id='ninos-input', type='number', value=0, step=1)
    ], style={'display': 'inline-block'}),
    html.Div([
        html.Label('Monto Alquiler o Crédito:'),
        dcc.Input(id='alquiler-input', type='number', value=0, step=10000)
    ], style={'display': 'inline-block'}),
    html.Button('Calcular', id='submit-val', n_clicks=0, style={'display': 'inline-block'}),
    dcc.Graph(id='piramide-grafico'),
    html.Div(id='output-container', style={'textAlign': 'center'})  # Contenedor para la imagen
    ])

    # Callback de Dash
    @dash_app.callback(
        [dash.dependencies.Output('piramide-grafico', 'figure'),
         dash.dependencies.Output('output-container', 'children')],
        [dash.dependencies.Input('submit-val', 'n_clicks')],
        [dash.dependencies.State('salario-input', 'value'),
         dash.dependencies.State('adultos-input', 'value'),
         dash.dependencies.State('ninos-input', 'value'),
         dash.dependencies.State('alquiler-input', 'value')]
    )
    def update_figure(n_clicks, selected_salario,adultos,ninos,alquiler):
        # Definir los límites de la pirámide
        anchos_por_piso = [10, 8, 6, 4, 2, 0]
        piramide_familiar = armar_piramide (adultos,ninos,alquiler,cba,cbt)
        
         # Calcular la posición del usuario en la recta
        for i in range(1, len(piramide_familiar)):
            if selected_salario <= piramide_familiar[i]:
                # Interpolación lineal entre los puntos de la recta definidos por piramide[i-1] y piramide[i]
                y_usuario = i - 1 + (selected_salario - piramide_familiar[i-1]) / (piramide_familiar[i] - piramide_familiar[i-1])
                break
        else:
            y_usuario = len(piramide_familiar) - 1  # En caso de que el salario exceda el máximo en la pirámide

        figuras = []

        # Dibujar los pisos de la pirámide
        for i in range(len(clases_pisos)):
            figuras.append(go.Scatter(
                x=[-anchos_por_piso[i] / 2, anchos_por_piso[i] / 2],
                y=[i, i],
                mode='lines',
                line=dict(width=0, color=str(gradiente_color(i, len(clases_pisos)))),
                fill='tonexty',
                showlegend=False
            ))

        # Agregar el marcador para la ubicación del usuario
        figuras.append(go.Scatter(
            x=[0],
            y=[y_usuario],
            mode='markers+text',
            marker=dict(size=15, color='purple'),
            text=['Tu ubicación en la pirámide'],  
            textposition="top center",
            name='Acá estás vos y tu familia',
             
        ))
        
        

        # Actualizar los ticks del eje y con los valores calculados
        layout = go.Layout(
            xaxis=dict(visible=False),
            yaxis=dict(
                tickvals=list(range(len(clases_pisos))),
                #ticktext=[f"{clases_pisos[i]}, mínimo de ${piramide_familiar[i]:.2f}" for i in range(len(clases_pisos))],
                ticktext=[f"{clases_pisos[i]}" for i in range(len(clases_pisos))],
                range=[-0.5, len(clases_pisos)],
            ),
            margin=dict(l=50, r=50, t=0, b=0),
            height=400,
        )

        figure = go.Figure(data=figuras, layout=layout)
        salida = f"Con un salario de ${selected_salario}, vos y tu familia son .... '{clases_pisos[int(y_usuario)]}'."
        
      # Agregar la imagen a la salida si el botón ha sido presionado
        imagen_html = html.Img(src=get_image_for_position(y_usuario), style={'width': '20em', 'height': '20em'}) if n_clicks > 0 else ''

        output = html.Div([html.P(salida), imagen_html])

        return figure, output

    return dash_app


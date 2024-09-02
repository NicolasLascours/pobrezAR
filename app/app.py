from flask import Flask, render_template, request,redirect,url_for
from piramide_social import create_dash_app
from consulta_dolarhoy import get_usd_blue

app = Flask(__name__)
dolar = get_usd_blue("https://dolarhoy.com/")
# Integrar Dash en Flask
piramide_clases = ['Base','Línea de Indigencia', 'Línea de Pobreza', 'Clase Media Baja','Clase Media','Clase Media Alta']
cba = 131294
cbt = 291472
dash_app = create_dash_app(app,piramide_clases,cba,cbt)

@app.route('/')
def index():
    return render_template('index.html',dolar=dolar)

@app.route("/about")
def about():       
    return render_template('about.html',dolar=dolar)

if __name__ == '__main__':
    app.run(debug=True)
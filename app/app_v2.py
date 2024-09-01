from flask import Flask, render_template, request,redirect,url_for
from piramide_v2 import create_dash_app
from consulta_dolarhoy import get_usd_blue


app = Flask(__name__)
dolar = get_usd_blue("https://dolarhoy.com/")
# Integrar Dash en Flask
piramide_salarios = [0,773000,850000,1350000,2850000]
piramide_clases = ['Pobre', 'Clase Media Pobre', 'Clase Media', 'Clase Media Alta', 'Clase Alta']
dash_app = create_dash_app(app,piramide_salarios,piramide_clases)

@app.route('/')
def index():
    return render_template('index_2.html',dolar=dolar)


@app.route("/about")
def about():       
    return render_template('about.html',dolar=dolar)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, redirect, render_template
from consulta_dolarhoy import get_usd_blue
from piramide_social import piramide

app = Flask(__name__)

dolar = get_usd_blue("https://dolarhoy.com/")
    
@app.route('/')

def index():        
    return render_template('index.html',dolar=dolar)

@app.route('/calculate', methods=['POST'])
def calculate():
    salario = request.form.get('salario')  # Captura el valor del salario del formulario
    try:
        # Convertir el valor a tipo float, eliminando cualquier símbolo de moneda
        salario = float(salario.replace('$', '').replace(',', '').strip())
    except ValueError:
        salario = 0.0  # Valor por defecto en caso de error en la conversión
    piramide_social = [0,773000,850000,1350000,2850000]
    
    # Generar el gráfico con el salario
    grafico_path, piso = piramide(round(salario),piramide_social) #/ float(dolar['venta'])
    
    return render_template('calcular.html', grafico=grafico_path, piso=piso,dolar=dolar)


if __name__ == '__main__':
    app.run(debug=True)
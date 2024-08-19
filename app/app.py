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
    # Convertir el valor a tipo float, eliminando cualquier símbolo de moneda
    try:
        salario = float(salario.replace('$', '').replace(',', '').strip())
    except ValueError:
        salario = 0.0  # Valor por defecto en caso de error en la conversión
    
    # Generar el gráfico con el salario
    print(dolar)
    grafico_path = piramide(round(salario)) #/ float(dolar['venta'])
    
    return render_template('calcular.html', grafico=grafico_path)


if __name__ == '__main__':
    app.run(debug=True)
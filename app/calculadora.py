from app.consulta_dolarhoy import get_usd_blue
from app.piramide_social import piramide




def calculate(salary):
        dolar = float(get_usd_blue(base_url)['compra'])
        return round(salary / dolar, 2)
        
if __name__ == "__main__":
    salario = calculate(500000)
    piramide(salario)
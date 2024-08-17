import requests
from bs4 import BeautifulSoup
import ssl

def get_usd_blue(base_url):
    # Evitar errores de certificados inexistentes en algunas páginas web
    ssl._create_default_https_context = ssl._create_unverified_context

    # Define el encabezado User-Agent
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Realiza la solicitud a la página
    response = requests.get(base_url, headers=headers)  # Agrega el encabezado a la solicitud
    try:
       
        # Parseamos el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Selecciona el bloque que contiene la información del Dólar Blue
        dolar_blue_section = soup.select_one('div.tile.is-child.only-mobile a[href="/cotizaciondolarblue"]')
        
        try:
            
            # Extrae la información de compra y venta
            dolar = {}
            titulo = dolar_blue_section.get_text(strip=True)
            dolar['compra'] = dolar_blue_section.find_next('div', class_='compra').find('div', class_='val').get_text(strip=True).replace("$", "")
            dolar['venta'] = dolar_blue_section.find_next('div', class_='venta').find('div', class_='val').get_text(strip=True).replace("$", "")
            return dolar
        except:
            return("No se encontró la sección de Dólar Blue.")
    except:
        return (f"Error al obtener la página. Código de estado: {response.status_code}")
    
    
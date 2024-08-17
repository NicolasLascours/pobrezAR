import matplotlib.pyplot as plt
import re
import io
import base64

def determinar_piso(valor):
    valor = float(valor)
    if valor < 500:
        return 1
    elif valor < 1000:
        return 2
    elif valor < 2000:
        return 3
    elif valor < 5000:
        return 4
    else:
        return 5

def gradiente_color(nivel, pisos):
    # Genera un color en el gradiente de rojo a verde
    red = (pisos - nivel) / (pisos - 1)
    green = (nivel - 1) / (pisos - 1)
    return (red, green, 0)  # Color en formato RGB


def piramide(salario):
    # Asegúrate de que salario sea una cadena
    salario = str(salario)
    
    # Eliminar el símbolo de pesos del salario
    salario_numerico = re.sub(r'[$]', '', salario)
    
    # Convertir a valor numérico
    salario_numerico = float(salario_numerico)
    
    # Determinar el piso del salario
    piso_salario = determinar_piso(salario_numerico)
    
    # Configuraciones de la pirámide
    pisos = 5
    anchos_por_piso = [10, 8, 6, 4, 2]  # Ancho de cada línea para cada piso
    altura_segmento = 2  # Altura de cada segmento

    # Crear una imagen en memoria
    img = io.BytesIO()
    
    # Dibujar la pirámide con líneas más altas
    plt.figure(figsize=(6, 4))  # Aumentar el tamaño de la figura

     # Establecer el fondo transparente
    plt.gca().patch.set_facecolor('none')
    plt.gcf().patch.set_facecolor('none')
    
    # Dibujar la estructura de la pirámide con líneas más altas
    for piso, ancho in enumerate(anchos_por_piso, start=1):
        y_base = (piso - 1) * altura_segmento  # Base del segmento
        y_top = piso * altura_segmento         # Top del segmento
        color = gradiente_color(piso, pisos)   # Obtener el color del gradiente
        plt.fill_between([-ancho/2, ancho/2], y_base, y_top, color=color, edgecolor='black')

    # Agregar el punto del salario en la pirámide
    y_pos = (piso_salario - 0.5) * altura_segmento
    plt.scatter(0, y_pos, color='purple', s=200, edgecolor='black')
    
    # Anotación del punto
    plt.annotate('Usted está aquí', 
                 xy=(0, y_pos), 
                 xytext=(0, y_pos + altura_segmento / 2), 
                 textcoords='offset points',
                 ha='center', 
                 va='bottom',
                 fontsize=12, 
                 color='black', 
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # Configuraciones de la gráfica
    plt.title("Pirámide Social de 5 Pisos")
    plt.xlabel("Posición Horizontal")
    plt.ylabel("Altura de los Pisos")
    plt.xticks([])
    plt.yticks([(i - 0.5) * altura_segmento for i in range(1, pisos + 1)], [f'Piso {i}' for i in range(1, pisos + 1)])
    plt.legend([f'Salario: ${salario_numerico}'], loc='upper right')
    
    # Guardar la imagen en el objeto BytesIO
    plt.savefig(img, format='png')
    plt.close()  # Cerrar la figura
    
    # Obtener la imagen en formato base64
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    return img_base64

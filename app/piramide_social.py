import matplotlib.pyplot as plt
import re
import io
import base64

def determinar_piso(salario,pisos):
    for i in range(len(pisos)):
        if salario < pisos[i]:
            return i + 1
    return len(pisos) + 1 

def gradiente_color(nivel, pisos):
    # Genera un color en el gradiente de rojo a verde
    red = (pisos - nivel) / (pisos - 1)
    green = (nivel - 1) / (pisos - 1)
    return (red, green, 0)  # Color en formato RGB

def piramide(salario,piramide_social):
    # Determinar el piso del salario
    piso_salario = determinar_piso(salario,piramide_social)
    
    # Configuraciones de la pirámide
    pisos = 5
    anchos_por_piso = [10, 8, 6, 4, 2]  # Ancho de cada línea para cada piso
    altura_segmento = 2  # Altura de cada segmento

    # Crear una imagen en memoria
    img = io.BytesIO()
    
    # Dibujar la pirámide con líneas 
    plt.figure(figsize=(6, 4))  

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
    plt.title("Pirámide Social")
    #plt.xlabel("Posición Horizontal")
    #plt.ylabel("Altura de los Pisos")
    plt.xticks([])

    # Etiquetas personalizadas para los pisos que coinciden con los estamentos sociales
    etiquetas_pisos = ['Clase Baja: $'+str(piramide_social[0]), 'Clase Media Baja: $'+str(piramide_social[1]), 'Clase Media: $'+str(piramide_social[2]), 'Clase Media Alta: $'+str(piramide_social[3]), 'Clase Alta: >'+str(piramide_social[3])]
    plt.yticks([(i - 0.5) * altura_segmento for i in range(1, pisos + 1)], etiquetas_pisos)
    
    plt.legend([f'Salario: ${salario}'], loc='upper right')
    
    plt.tight_layout()

    # Guardar la imagen en el objeto BytesIO
    plt.savefig(img, format='png')
    plt.close()  # Cerrar la figura
    
    # Obtener la imagen en formato base64
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    return img_base64

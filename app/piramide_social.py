import matplotlib.pyplot as plt
import io
import base64

def determinar_piso(salario, salario_pisos):
    for i in range(len(salario_pisos) - 1):
        if salario_pisos[i] <= salario < salario_pisos[i + 1]: #verifica si el salario cae entre dos valores consecutivos
            return i + 1
    return len(salario_pisos)


def gradiente_color(nivel, pisos):
    # Genera un color en el gradiente de rojo a verde
    red = (pisos - nivel) / (pisos - 1)
    green = (nivel - 1) / (pisos - 1)
    return (red, green, 0)  # Color en formato RGB

def piramide(salario, piramide_salarios):
    # Determinar el piso del salario
    piramide_clases = ['Clase Baja', 'Clase Media Baja', 'Clase Media', 'Clase Media Alta', 'Clase Alta']
    estrato_usuario = determinar_piso(salario, piramide_salarios)

    # Configuraciones de la pirámide
    pisos = len(piramide_clases)
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
    y_pos = (estrato_usuario - 0.5) * altura_segmento
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

    # Eliminar etiquetas del eje X
    plt.xticks([])

    # Etiquetas personalizadas para los pisos que coinciden con los estamentos sociales
    etiquetas_pisos = []
    for i in range(0, len(piramide_clases)):
        etiquetas_pisos.append(piramide_clases[i] + ': $' + str(piramide_salarios[i]))
    plt.yticks([(i - 1) * altura_segmento for i in range(1, pisos + 1)], etiquetas_pisos)
    
    #plt.legend([f'Salario: ${salario}'], loc='upper right')
    
    plt.tight_layout()

    # Guardar la imagen en el objeto BytesIO
    plt.savefig(img, format='png')
    plt.close()  # Cerrar la figura
    
    # Obtener la imagen en formato base64
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    return img_base64, piramide_clases[estrato_usuario-1]

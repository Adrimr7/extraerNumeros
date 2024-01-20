import os
import re
import easyocr
from concurrent.futures import ProcessPoolExecutor

def extraer_numeros(texto):
    numeros = re.findall(r'\d+', texto)
    return ' '.join(numeros)

def procesar_imagen(ruta_imagen):
    lector = easyocr.Reader(['en'])
    resultados = lector.readtext(ruta_imagen)
    texto = ' '.join([resultado[1] for resultado in resultados])
    return texto

def procesar_carton(i):
    ruta_carpeta = r'la_ruta_de_la_carpeta'
    nombre_imagen = f'carton ({i}).jpg'
    ruta_imagen = os.path.join(ruta_carpeta, nombre_imagen)
    texto = procesar_imagen(ruta_imagen)
    nums = extraer_numeros(texto)
    return nums

if __name__ == "__main__":

    ruta_carpeta = r'la_ruta_de_la_carpeta'
    nombre_archivo_total = 'solo_numeros.txt'
    total_cartones = 135
    with ProcessPoolExecutor() as executor:
        resultados = list(executor.map(procesar_carton, range(1, total_cartones + 1)))
    resultados_filtrados = filter(None, resultados)
    with open(os.path.join(ruta_carpeta, nombre_archivo_total), 'w') as archivo:
        archivo.write('\n\n'.join(resultados_filtrados))

    print("Proceso completado. Solo los números extraídos han sido guardados en un solo archivo.")

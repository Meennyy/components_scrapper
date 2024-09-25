import os
import re
from dotenv import load_dotenv
from colorama import Fore, init
import requests

# Cargar variables de entorno
load_dotenv()

# Inicializar colorama para los colores en la terminal
init(autoreset=True)

# Obtener la URL base desde el archivo .env
base_url = os.getenv("WEBSITE_URL")

# Expresión regular para capturar nombres de tarjetas gráficas, precios y existencia
patron = r"Tarjeta de Video\s*([A-Za-z0-9\s\-]+(?:NVIDIA|AMD|GeForce|Radeon|RTX|GTX|RX|Vega|Quadro|FirePro)\s*[A-Za-z0-9\s\-\/\.]+).*?(\$[0-9,.]+).*?(CON EXISTENCIA|SIN EXISTENCIA)"
todas_las_tarjetas = set()  # Usar un conjunto para eliminar duplicados

# Definir el número máximo de páginas a recorrer
num_paginas = 10  # Cambiar este número según tus necesidades

# Función para obtener tarjetas gráficas de una página
def obtener_tarjetas(pagina):
    paginado = os.getenv("WEBSITE_URL_PAGINADO")
    pagina_url = f"{paginado}{pagina}"
    content = requests.get(pagina_url).text
    return re.findall(patron, content, re.DOTALL)

# Bucle para recorrer cada página del paginador
for pagina in range(1, num_paginas + 1):
    matches = obtener_tarjetas(pagina)
    # Limpiar espacios y agregar a la lista como tupla
    for tarjeta, precio, existencia in matches:
        tarjeta = tarjeta.strip()  # Eliminar espacios
        precio = precio.strip()     # Eliminar espacios
        existencia = existencia.strip()  # Eliminar espacios
        todas_las_tarjetas.add((tarjeta, precio, existencia))  # Almacenar como tupla en un conjunto

# Variables de búsqueda
criterios = {
    "modelo": "4060",  # Buscando tarjetas con '4060'
    "marca": "ASUS",   # Buscando tarjetas ASUS
    "vram": "8GB",     # Buscando tarjetas con 8GB de VRAM
}

# Filtrar resultados basados en los criterios de búsqueda
resultados = [
    (tarjeta, precio, existencia) 
    for tarjeta, precio, existencia in todas_las_tarjetas
    if all(criterio.lower() in tarjeta.lower() for criterio in criterios.values())
]

# Muestra los resultados encontrados
if resultados:
    print(Fore.GREEN + "\nTarjetas gráficas encontradas que cumplen con los criterios:\n")
    for resultado, precio, existencia in resultados:
        print(f"{Fore.YELLOW + resultado} - {Fore.GREEN + precio} - {Fore.BLUE + existencia}")
else:
    print(Fore.RED + "\nNo se encontraron tarjetas gráficas que cumplan con los criterios.")

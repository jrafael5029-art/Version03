# ============================================================
# RECONOCIMIENTO DE SEÑALES DE TRÁNSITO - VERSIÓN 3
# Dataset alojado en Google Drive (carpetas públicas)
#
# Librerías necesarias:
#   - gdown       : descargar carpetas de Google Drive  ← INSTALAR (ver abajo)
#   - matplotlib  : mostrar imágenes en gráfico          ← ya viene en Anaconda
#   - PIL         : abrir imágenes                        ← ya viene en Anaconda
#   - os          : manejo de rutas                       ← ya viene en Python
#
# INSTALACIÓN ÚNICA (ejecutar UNA sola vez en Anaconda Prompt):
#   pip install gdown
# ============================================================

import os
import gdown
import matplotlib.pyplot as plt
from PIL import Image

# ------------------------------------------------------------
# CONFIGURACIÓN — pega aquí los IDs de tus carpetas de Drive
#
# ¿Cómo obtener el ID de una carpeta de Google Drive?
#   1. Abre la carpeta en Google Drive
#   2. Clic derecho → "Obtener enlace"
#   3. Asegúrate que esté en "Cualquier persona con el enlace"
#   4. El enlace se ve así:
#      https://drive.google.com/drive/folders/1ABC...XYZ?usp=sharing
#                                              ↑ ese es el ID
# ------------------------------------------------------------

CARPETAS_DRIVE = {
    "Pare"      : "https://drive.google.com/drive/folders/1oPW3YgON1bzBXn9WjR6Hi5ZtYpOVrhmW?usp=sharing",
    "Limite_60" : "https://drive.google.com/drive/folders/1ua8dYI8iATip-xPaNmwo2ArA2_0-oRrq?usp=sharing",
}

# Carpeta local donde se descargarán las imágenes temporalmente
RUTA_DESCARGA = r"C:\Users\USUARIO\Desktop\Dataset_descargado"

EXTENSIONES = (".jpg", ".jpeg", ".png", ".bmp")

# ------------------------------------------------------------
# FUNCIÓN 1: Descargar carpeta desde Google Drive
# Usa gdown para descargar todos los archivos de una carpeta pública
# ------------------------------------------------------------

def descargar_carpeta(clase, folder_id, ruta_base):
    ruta_destino = os.path.join(ruta_base, clase)
    os.makedirs(ruta_destino, exist_ok=True)

    # Si ya fue descargada antes, no vuelve a descargar
    archivos_existentes = [f for f in os.listdir(ruta_destino)
                           if f.lower().endswith(EXTENSIONES)]
    if archivos_existentes:
        print(f"[INFO] '{clase}' ya descargada → {len(archivos_existentes)} imagen(es) en caché")
        return ruta_destino

    print(f"[DESCARGA] Descargando carpeta '{clase}' desde Google Drive...")
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    gdown.download_folder(url, output=ruta_destino, quiet=False, use_cookies=False)
    return ruta_destino

# ------------------------------------------------------------
# FUNCIÓN 2: Cargar dataset (descargar si es necesario)
# Retorna: { "Pare": ["img1.jpg", ...], "Limite_60": [...] }
# ------------------------------------------------------------

def cargar_dataset():
    dataset = {}
    for clase, folder_id in CARPETAS_DRIVE.items():
        ruta_clase = descargar_carpeta(clase, folder_id, RUTA_DESCARGA)
        imagenes   = sorted([f for f in os.listdir(ruta_clase)
                              if f.lower().endswith(EXTENSIONES)])
        dataset[clase] = imagenes
        print(f"[INFO] Clase '{clase}' → {len(imagenes)} imagen(es) lista(s)")
    return dataset

# ------------------------------------------------------------
# FUNCIÓN 3: Reconocer señal por nombre de archivo
# Nivel 1 — el archivo existe en alguna clase del dataset
# Nivel 2 — el nombre de la señal aparece en el nombre del archivo
# Nivel 3 — no reconocida
# ------------------------------------------------------------

def reconocer_senal(nombre_imagen, dataset):
    # Nivel 1: coincidencia exacta
    for clase, imagenes in dataset.items():
        if nombre_imagen in imagenes:
            return clase, "Coincidencia exacta"

    # Nivel 2: coincidencia por nombre
    for clase in dataset:
        if clase.lower() in nombre_imagen.lower():
            return clase, "Coincidencia por nombre"

    # Nivel 3: no reconocida
    return "Desconocida", "No reconocida en el dataset"

# ------------------------------------------------------------
# FUNCIÓN 4: Mostrar TODAS las imágenes de la clase reconocida
# ------------------------------------------------------------

def mostrar_imagenes_clase(clase, dataset):
    if clase == "Desconocida" or clase not in dataset:
        print(f"[AVISO] No se pueden mostrar imágenes de '{clase}'.")
        return

    imagenes = dataset[clase]
    total    = len(imagenes)
    cols     = min(total, 4)
    rows     = (total + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3))
    fig.suptitle(f"Señal reconocida: {clase}  ({total} imagen(es))",
                 fontsize=14, fontweight="bold", color="darkred")
    fig.patch.set_facecolor("#f0f0f0")

    # Normalizar axes a lista plana
    ax_list = []
    if rows == 1 and cols == 1:
        ax_list = [axes]
    elif rows == 1:
        ax_list = list(axes)
    else:
        for fila in axes:
            ax_list.extend(list(fila) if hasattr(fila, '__iter__') else [fila])

    for i, nombre in enumerate(imagenes):
        ruta_img = os.path.join(RUTA_DESCARGA, clase, nombre)
        img = Image.open(ruta_img)
        ax_list[i].imshow(img)
        ax_list[i].set_title(nombre, fontsize=8)
        ax_list[i].axis("off")

    for j in range(total, len(ax_list)):
        ax_list[j].axis("off")

    plt.tight_layout()
    plt.show()

# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------

print("=" * 52)
print("   RECONOCIMIENTO DE SEÑALES DE TRÁNSITO")
print("   Fuente: Google Drive (nube)")
print("=" * 52)

# Paso 1: descargar y cargar dataset desde Drive
dataset = cargar_dataset()

total_imagenes = sum(len(v) for v in dataset.values())
print(f"\n   Clases  : {list(dataset.keys())}")
print(f"   Imágenes: {total_imagenes} en total")
print("=" * 52)

# Paso 2: simular entradas
# → Cambia estos nombres por los de tus archivos reales en Drive
entradas_prueba = [
    "pare_01.jpg",
    "limite_60_01.png",
]

# Paso 3: reconocer y mostrar gráfico
for entrada in entradas_prueba:
    clase, tipo = reconocer_senal(entrada, dataset)

    print(f"\n  Imagen entrada  : {entrada}")
    print(f"  Señal reconocida: {clase}  ({tipo})")
    print("-" * 52)

    mostrar_imagenes_clase(clase, dataset)

print("\n" + "=" * 52)
print("  Las imágenes quedan en caché local para uso offline.")
print("=" * 52)
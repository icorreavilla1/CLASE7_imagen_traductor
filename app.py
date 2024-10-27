import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

# Variable para texto OCR
text = " "

# Función para convertir texto a audio
def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    my_file_name = text[0:20] if len(text) > 20 else "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

# Eliminar archivos antiguos en la carpeta temporal
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    now = time.time()
    n_days = n * 86400
    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)
            print("Deleted ", f)

# Eliminar archivos mp3 después de 7 días
remove_files(7)

# Título y subtítulo de la aplicación
st.title("🔍 Reconocimiento Óptico de Caracteres y Traducción")
st.markdown("#### Detecta y traduce texto de una imagen, con opción de salida en audio 🔊")

# Opciones de entrada de imagen: cámara o archivo
st.subheader("Selecciona la fuente de la imagen:")
cam_ = st.checkbox("Usar Cámara")
img_file_buffer = st.camera_input("Toma una Foto") if cam_ else None

# Barra lateral para configuración
with st.sidebar:
    st.header("⚙️ Opciones de Procesamiento")
    filtro = st.radio("Aplicar filtro en imagen de cámara", ('Sí', 'No'))

# Carga de imagen desde archivo
bg_image = st.file_uploader("Cargar Imagen:", type=["png", "jpg"])
if bg_image is not None:
    st.image(bg_image, caption='Imagen cargada.', use_column_width=True)
    with open(bg_image.name, 'wb') as f:
        f.write(bg_image.read())
    st.success(f"✅ Imagen guardada como {bg_image.name}")
    img_cv = cv2.imread(bg_image.name)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("**Texto Detectado:**")
    st.write(text)

# Procesamiento de imagen de cámara
if img_file_buffer:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    cv2_img = cv2.bitwise_not(cv2_img) if filtro == 'Sí' else cv2_img
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.markdown("**Texto Detectado:**")
    st.write(text)

# Parámetros de traducción y audio en la barra lateral
with st.sidebar:
    st.header("🌐 Parámetros de Traducción y Audio")
    os.makedirs("temp", exist_ok=True)
    
    # Selección de idioma de entrada
    translator = Translator()
    in_lang = st.selectbox("Selecciona el idioma de entrada:", ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"))
    input_language = {'Inglés': 'en', 'Español': 'es', 'Bengalí': 'bn', 'Coreano': 'ko', 'Mandarín': 'zh-cn', 'Japonés': 'ja'}[in_lang]
    
    # Selección de idioma de salida
    out_lang = st.selectbox("Selecciona el idioma de salida:", ("Inglés", "Español", "Bengalí", "Coreano", "Mandarín", "Japonés"))
    output_language = {'Inglés': 'en', 'Español': 'es', 'Bengalí': 'bn', 'Coreano': 'ko', 'Mandarín': 'zh-cn', 'Japonés': 'ja'}[out_lang]
    
    # Selección de acento en inglés
    english_accent = st.selectbox("Selecciona el acento en inglés (si aplica):", ["Default", "India", "United Kingdom", "United States", "Canada", "Australia", "Ireland", "South Africa"])
    tld = {'Default': 'com', 'India': 'co.in', 'United Kingdom': 'co.uk', 'United States': 'com', 'Canada': 'ca', 'Australia': 'com.au', 'Ireland': 'ie', 'South Africa': 'co.za'}[english_accent]
    
    # Mostrar texto traducido
    display_output_text = st.checkbox("Mostrar texto traducido")

    # Botón para iniciar conversión
    if st.button("Convertir Texto a Audio"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("### 🔉 Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
        
        if display_output_text:
            st.markdown("### Texto traducido:")
            st.write(output_text)





 
    
    

import streamlit as st
from pydub import AudioSegment
import tempfile
import os

st.set_page_config(page_title="Conversor de Audio", page_icon="🎵", layout="centered")
st.title("🎵 Conversor de Audio en Línea")

st.write("Sube un archivo de audio y conviértelo a otro formato directamente desde tu navegador.")

# Subida del archivo
archivo_subido = st.file_uploader("Selecciona un archivo de audio", type=["opus", "mp3", "wav", "flac", "m4a", "ogg"])
formato_salida = st.selectbox("Formato de salida", ["mp3", "wav", "flac", "ogg"])

if archivo_subido:
    with tempfile.NamedTemporaryFile(delete=False, suffix="." + archivo_subido.name.split(".")[-1]) as entrada:
        entrada.write(archivo_subido.read())
        ruta_entrada = entrada.name

    ruta_salida = ruta_entrada.rsplit(".", 1)[0] + "." + formato_salida

    try:
        # Conversión usando pydub (requiere ffmpeg instalado en el servidor)
        audio = AudioSegment.from_file(ruta_entrada)
        audio.export(ruta_salida, format=formato_salida)

        # Botón de descarga
        with open(ruta_salida, "rb") as f:
            st.download_button(
                label="⬇️ Descargar archivo convertido",
                data=f,
                file_name=os.path.basename(ruta_salida),
                mime="audio/" + formato_salida
            )

        st.success("✅ Conversión completada")
    except Exception as e:
        st.error(f"❌ Error en la conversión: {e}")

    # Limpieza de archivos temporales
    os.remove(ruta_entrada)
    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)

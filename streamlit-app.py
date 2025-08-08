import streamlit as st
from pydub import AudioSegment
import tempfile
import os

st.set_page_config(page_title="Conversor de Audio", page_icon="🎵", layout="centered")
st.title("🎵 Conversor de Audio en Línea (Múltiples Archivos)")

st.write("Sube uno o varios archivos de audio y conviértelos a otro formato. El nombre original se mantendrá.")

# Subida de múltiples archivos
archivos_subidos = st.file_uploader(
    "Selecciona uno o varios archivos de audio",
    type=["opus", "mp3", "wav", "flac", "m4a", "ogg"],
    accept_multiple_files=True
)
formato_salida = st.selectbox("Formato de salida", ["mp3", "wav", "flac", "ogg"])

if archivos_subidos:
    for archivo in archivos_subidos:
        # Nombre base sin extensión
        nombre_base = os.path.splitext(archivo.name)[0]

        # Guardar archivo temporal de entrada
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + archivo.name.split(".")[-1]) as entrada:
            entrada.write(archivo.read())
            ruta_entrada = entrada.name

        # Ruta temporal de salida
        ruta_salida = os.path.join(tempfile.gettempdir(), nombre_base + "." + formato_salida)

        try:
            # Conversión con pydub
            audio = AudioSegment.from_file(ruta_entrada)
            audio.export(ruta_salida, format=formato_salida)

            # Botón de descarga para cada archivo
            with open(ruta_salida, "rb") as f:
                st.download_button(
                    label=f"⬇️ Descargar {nombre_base}.{formato_salida}",
                    data=f,
                    file_name=f"{nombre_base}.{formato_salida}",
                    mime="audio/" + formato_salida
                )

            st.success(f"✅ {archivo.name} convertido con éxito.")
        except Exception as e:
            st.error(f"❌ Error con {archivo.name}: {e}")

        # Limpieza de archivos temporales
        os.remove(ruta_entrada)
        if os.path.exists(ruta_salida):
            os.remove(ruta_salida)

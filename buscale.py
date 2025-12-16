import pandas as pd
import sqlite3
import streamlit as st
import re
import unicodedata

st.set_page_config(page_title="Analizador de Cocina", layout="centered", page_icon="🍳")

SQLITE_DB = "cocina.db"


# ===============================
# Normalizar texto
# ===============================
def limpiar_texto(texto: str) -> str:
    nfkd = unicodedata.normalize('NFKD', texto)
    texto = "".join(c for c in nfkd if not unicodedata.combining(c))
    texto = texto.lower()
    texto = re.sub(r"[^a-zñ\s]", "", texto)
    return texto


# ===============================
# Cargar palabras desde SQLite
# ===============================
def cargar_palabras_cocina():
    conn = sqlite3.connect(SQLITE_DB)
    df = pd.read_sql_query("SELECT palabra FROM palabras", conn)
    conn.close()
    return df["palabra"].tolist()


# ===============================
# Analizar coincidencias contra la BD (✅ PORCENTAJE CORRECTO)
# ===============================
def analizar_texto_cocina(texto: str, palabras_cocina: list):
    texto_limpio = limpiar_texto(texto)
    palabras_texto = texto_limpio.split()  # 👈 YA NO ES SET PARA CONTAR BIEN
    palabras_bd = set(palabras_cocina)

    if not palabras_bd or not palabras_texto:
        return 0, []

    total_palabras_texto = len(palabras_texto)

    coincidencias = []
    for palabra in palabras_texto:
        if palabra in palabras_bd:
            coincidencias.append(palabra)

    total_coincidencias = len(coincidencias)

    porcentaje = (total_coincidencias / total_palabras_texto) * 100  # ✅ AQUÍ YA ESTA BIEN

    return round(porcentaje, 2), sorted(set(coincidencias)), total_coincidencias, total_palabras_texto


# ===============================
# APP PRINCIPAL
# ===============================
def app():
    st.title("🍳 Analizador de Texto de Cocina")
    st.caption("Analiza qué tanto se relaciona tu texto con el diccionario de cocina")

    palabras_cocina = cargar_palabras_cocina()
    total_bd = len(palabras_cocina)

    st.info(f"📚 Palabras en la base de datos: {total_bd}")

    texto_usuario = st.text_area(
        "✍️ Escribe o pega tu texto:",
        height=200,
        placeholder="Ejemplo: Hoy voy a freír cebolla en el sartén para hacer una salsa verde..."
    )

    if st.button("🔍 Analizar"):
        if not texto_usuario.strip():
            st.warning("⚠️ Por favor ingresa un texto.")
            return

        porcentaje, coincidencias, total_coincidencias, total_palabras = analizar_texto_cocina(
            texto_usuario, palabras_cocina
        )

        # ===============================
        # RESULTADOS
        # ===============================
        st.subheader("📊 Resultado del análisis")

        st.metric("Relación con cocina", f"{porcentaje} %")
        st.write(f"✅ Coincidencias encontradas: **{total_coincidencias} de {total_palabras} palabras del texto**")

        if porcentaje >= 20:
            st.success("✅ Tu texto está claramente relacionado con cocina 🍽️")
        elif porcentaje >= 5:
            st.warning("⚠️ Tu texto tiene relación leve con cocina")
        else:
            st.error("❌ Tu texto casi no tiene relación con cocina")

        st.subheader("🔎 Palabras detectadas")
        if coincidencias:
            st.write(", ".join(coincidencias))
        else:
            st.info("No se detectaron términos de cocina en el texto.")


if __name__ == "__main__":
    app()

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pydeck

# Configuración de la página
st.set_page_config(page_title="Scrambuster 60+", page_icon="🛡️", layout="centered")

# Inicializa el estado del mensaje y otros elementos
if "mensaje_guardado" not in st.session_state:
    st.session_state["mensaje_guardado"] = ""
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = 0
if "juego_puntaje" not in st.session_state:
    st.session_state.juego_puntaje = 0
if "datos" not in st.session_state:
    st.session_state.datos = []

palabras_peligrosas = [
    "urgente", "clic aquí", "premio", "cuenta bloqueada", "verifica", "regalo",
    "bonificación", "transferencia", "datos personales", "confirmar tu identidad",
    "has sido seleccionado", "seguridad bancaria", "problemas con tu cuenta"
]

# Título principal
st.markdown("## 🛡️ Scrambuster 60+")
st.markdown("### Detector de mensajes sospechosos en redes sociales")
st.info("👵👴 Herramienta pensada para adultos mayores. Copia aquí el mensaje que recibiste y lo analizaremos por ti.")

# Área de texto
mensaje = st.text_area("✉️ Escribe o pega el mensaje aquí:", value=st.session_state["mensaje_guardado"], height=150)

# Botones
col1, col2 = st.columns(2)
with col1:
    analizar = st.button("🔍 Analizar mensaje")
with col2:
    limpiar = st.button("🧹 Limpiar mensaje")

# Lógica del botón "Analizar"
if analizar:
    st.session_state["mensaje_guardado"] = mensaje
    if mensaje.strip() == "":
        st.warning("⚠️ Por favor, escribe o pega un mensaje para analizar.")
    else:
        es_malicioso = any(p in mensaje.lower() for p in palabras_peligrosas)
        if es_malicioso:
            st.markdown("""
            <div style='padding:15px; background-color:#ffe6e6; border-radius:10px'>
                <h3 style='color:#b30000'>🚨 ¡Alerta! Mensaje posiblemente malicioso</h3>
                <p>No hagas clic en enlaces ni compartas datos personales.</p>
                <ul>
                    <li>✅ No respondas al mensaje.</li>
                    <li>🔒 Cambia tus contraseñas si ya diste información.</li>
                    <li>📞 Reporta el incidente a tu banco o institución correspondiente.</li>
                    <li>🛡️ Considera instalar herramientas de seguridad digital.</li>
                    <li>📚 Infórmate más en nuestro sitio para prevenir fraudes futuros.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='padding:15px; background-color:#e6ffe6; border-radius:10px'>
                <h3 style='color:#267326'>✅ Este mensaje parece confiable</h3>
                <p>Aun así, actúa con precaución.</p>
            </div>
            """, unsafe_allow_html=True)

# Lógica del botón "Limpiar"
if limpiar:
    st.session_state["mensaje_guardado"] = ""
    st.info("🧹 El mensaje ha sido borrado. Puedes escribir uno nuevo.")

# Juego de práctica de clasificación
st.markdown("---")
st.header("🎮 Juego: ¿Este mensaje es malicioso?")
mensajes_juego = [
    ("Has ganado un premio, haz clic aquí para reclamar.", "Malicioso"),
    ("Hola, ¿quieres salir a caminar hoy?", "No malicioso"),
    ("Verifica tu cuenta para evitar bloqueos.", "Malicioso"),
    ("Te espero a las 5 en el parque.", "No malicioso")
]

if st.session_state.pregunta_actual < len(mensajes_juego):
    mensaje_j, respuesta_correcta = mensajes_juego[st.session_state.pregunta_actual]
    st.markdown(f"**Mensaje:** {mensaje_j}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 Malicioso"):
            if respuesta_correcta == "Malicioso":
                st.success("✅ Correcto")
                st.session_state.juego_puntaje += 1
            else:
                st.error("❌ Incorrecto")
    with col2:
        if st.button("✅ No malicioso"):
            if respuesta_correcta == "No malicioso":
                st.success("✅ Correcto")
                st.session_state.juego_puntaje += 1
            else:
                st.error("❌ Incorrecto")
    if st.button("Siguiente pregunta"):
        st.session_state.pregunta_actual += 1
else:
    st.success(f"🎉 Juego terminado. Puntaje: {st.session_state.juego_puntaje}/{len(mensajes_juego)}")
    if st.button("Reiniciar juego"):
        st.session_state.pregunta_actual = 0
        st.session_state.juego_puntaje = 0

# Sección de predicción por alcaldía y hora
st.markdown("---")
st.header("📍 Predicción de fraude por alcaldía")

alcaldias_posibles = [
    'CUAUHTEMOC', 'LA MAGDALENA CONTRERAS', 'BENITO JUAREZ',
    'IZTAPALAPA', 'GUSTAVO A. MADERO', 'MIGUEL HIDALGO', 'COYOACAN',
    'TLAHUAC', 'CUAJIMALPA DE MORELOS', 'TLALPAN', 'MILPA ALTA',
    'VENUSTIANO CARRANZA', 'AZCAPOTZALCO', 'ALVARO OBREGON',
    'XOCHIMILCO', 'CDMX'
]
horas_numericas = list(range(0, 24))
hora_dict = {f"{h:02d}:00": h for h in horas_numericas}

alcaldia = st.selectbox("Selecciona una alcaldía:", alcaldias_posibles)
hora = st.selectbox("Selecciona una hora:", list(hora_dict.keys()))

np.random.seed(42)  # Reproducibilidad
data_simulada = pd.DataFrame({
    "alcaldia_hecho": np.random.choice(alcaldias_posibles, 5000),
    "hora": np.random.choice(horas_numericas, 5000),
    "fraude_ocurrido": np.random.binomial(1, 0.2, 5000)
})

filtrado = data_simulada[
    (data_simulada["alcaldia_hecho"] == alcaldia) &
    (data_simulada["hora"] == hora_dict[hora])
]

probabilidad = filtrado["fraude_ocurrido"].mean() if not filtrado.empty else 0
st.metric("Probabilidad estimada de fraude", f"{probabilidad*100:.1f}%")

def explicar_prediccion(filtrado, probabilidad):
    total = len(filtrado)
    casos_fraude = filtrado["fraude_ocurrido"].sum()
    return f"""
    <div style='background-color:#f9f9f9; padding:10px; border-radius:10px; border-left:5px solid #4CAF50;'>
        <b>¿Cómo se calcula?</b><br>
        De un total de <b>{total}</b> reportes simulados para esa alcaldía y hora, <b>{casos_fraude}</b> fueron fraudes reales.<br>
        Esto da una estimación de <b>{probabilidad*100:.1f}%</b>.
    </div>
    """

st.markdown(explicar_prediccion(filtrado, probabilidad), unsafe_allow_html=True)

# Visualización
conteo_fraude = data_simulada.groupby("alcaldia_hecho")["fraude_ocurrido"].mean().reset_index()
conteo_fraude.columns = ["Alcaldía", "Probabilidad"]
chart = alt.Chart(conteo_fraude).mark_bar().encode(
    x=alt.X("Alcaldía", sort="-y"),
    y=alt.Y("Probabilidad", title="Probabilidad de fraude"),
    color="Probabilidad",
    tooltip=["Alcaldía", "Probabilidad"]
).properties(
    width=600,
    height=400,
    title="Probabilidad promedio de fraude por alcaldía"
)
st.altair_chart(chart, use_container_width=True)

# Mapa interactivo con ubicaciones de fraude
st.markdown("### 🗺️ Mapa de reportes")

np.random.seed(123)
data_simulada["latitud"] = np.random.uniform(19.2, 19.5, size=len(data_simulada))
data_simulada["longitud"] = np.random.uniform(-99.25, -99.05, size=len(data_simulada))

layer = pydeck.Layer(
    "ScatterplotLayer",
    data=data_simulada[data_simulada["fraude_ocurrido"] == 1],
    get_position="[longitud, latitud]",
    get_radius=100,
    get_fill_color=[255, 0, 0, 160],
    pickable=True
)

view_state = pydeck.ViewState(
    latitude=19.4,
    longitude=-99.15,
    zoom=10,
    pitch=0
)

st.pydeck_chart(
    pydeck.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "Fraude reportado aquí"})
)



# Aviso de privacidad
st.markdown("---")
st.markdown("""
> Esta aplicación tiene fines **educativos y sin fines de lucro**. Los mensajes ingresados no se almacenan ni se comparten públicamente. Scrambuster 60+ protege tu privacidad y no expone tus datos.
""")

# Pie de página
st.caption("🔐 Scrambuster 60+ | Prevención de fraudes digitales para adultos mayores")










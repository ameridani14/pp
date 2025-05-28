import streamlit as st

# Función básica para detectar mensajes maliciosos (ejemplo simple)
def es_mensaje_malicioso(texto):
    palabras_clave = ["urgente", "clic aquí", "premio", "cuenta bloqueada", "verifica", "regalo"]
    for palabra in palabras_clave:
        if palabra.lower() in texto.lower():
            return True
    return False

# Título
st.title("Scrambuster 60+ 🛡️")
st.subheader("Detector de mensajes sospechosos en redes sociales")

# Instrucciones
st.markdown("Copia aquí un mensaje que hayas recibido y creas que puede ser malicioso:")

# Área de texto
mensaje = st.text_area("Mensaje recibido", height=150)

# Botón para analizar
if st.button("Analizar mensaje"):
    if mensaje.strip() == "":
        st.warning("Por favor, escribe o pega un mensaje para analizar.")
    elif es_mensaje_malicioso(mensaje):
        st.error("⚠️ Este mensaje podría ser malicioso. No hagas clic en enlaces ni compartas tus datos.")
    else:
        st.success("✅ Este mensaje no parece malicioso. Aun así, mantente alerta.")

# Pie de página
st.markdown("---")
st.caption("Scrambuster 60+ | Prevención de fraudes digitales para adultos mayores")




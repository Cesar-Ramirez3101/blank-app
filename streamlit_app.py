import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Generador de Informes Médicos - Aseguradoras", layout="wide")

st.title("🏥 Asistente Inteligente de Informes Médicos")
st.markdown("Sube el formato en blanco del informe y la nota de evolución para que la IA autogenere el documento listo para revisión.")

# Configurar la API Key (idealmente se guarda en los Secrets de Streamlit, pero puedes pedirla aquí o configurarla)
api_key = st.secrets.get("GEMINI_API_KEY") or st.text_input("Ingresa tu API Key de Google Gemini:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Plantilla del Informe (En blanco)")
        plantilla_texto = st.text_area("Pega aquí la estructura o campos del informe de la aseguradora en blanco:", height=250, placeholder="Ejemplo:\n- Nombre del paciente:\n- Diagnóstico (CIE-10):\n- Padecimiento Actual:\n- Evolución y Tratamiento:")

    with col2:
        st.subheader("2. Nota de Evolución (Llena)")
        nota_texto = st.text_area("Pega aquí la nota de evolución médica real:", height=250, placeholder="Ejemplo:\nPaciente acude por dolor abdominal de 3 días de evolución, signos vitales estables...")

    if st.button("✨ Generar Informe Autocompletado", type="primary"):
        if plantilla_texto and nota_texto:
            with st.spinner("Procesando información y redactando informe..."):
                try:
                    # Usamos Gemini para procesar la información
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    Actúa como un médico especialista experto en auditoría médica y llenado de formatos para aseguradoras.
                    Tu tarea es tomar la "Nota de Evolución" proporcionada y extraer/redactar la información necesaria para rellenar estrictamente la "Plantilla del Informe".
                    
                    Reglas:
                    - Mantén un lenguaje médico formal, técnico y preciso.
                    - No inventes datos que no estén en la nota de evolución; si falta un dato clave, déjalo marcado como [Pendiente/No especificado en nota].
                    - Respeta la estructura de la plantilla en blanco.
                    
                    PLANTILLA EN BLANCO:
                    {plantilla_texto}
                    
                    NOTA DE EVOLUCIÓN:
                    {nota_texto}
                    
                    INFORME AUTOCOMPLETADO:
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.success("¡Informe generado con éxito!")
                    st.subheader("3. Resultado Editable")
                    
                    # Cuadro de texto editable para ajustes manuales finales
                    informe_editado = st.text_area("Puedes revisar y editar libremente el informe antes de copiarlo o imprimirlo:", value=response.text, height=400)
                    
                    st.download_button(
                        label="📥 Descargar Informe como Texto",
                        data=informe_editado,
                        file_name="informe_medico_aseguradora.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Ocurrió un error al conectar con la IA: {e}")
        else:
            st.warning("Por favor, completa ambos campos (la plantilla y la nota de evolución).")
else:
    st.info("👆 Por favor ingresa tu API Key de Gemini para comenzar. Es gratuita y la obtienes en Google AI Studio.")

import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st # Importa Streamlit

# 1. Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Error: La clave API de OpenAI no se encontró en las variables de entorno. Asegúrate de tener un archivo .env con OPENAI_API_KEY='tu_clave_aqui'.")
    st.stop() # Detiene la ejecución si no hay API key

client = OpenAI(api_key=api_key)

# 2. Funciones de Carga y Procesamiento de Datos (Sin cambios importantes)
@st.cache_data # Cachea los datos para no recargarlos en cada interacción
def cargar_datos(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            datos = df.set_index('metrica')['valor'].to_dict()
            return datos
        except Exception as e:
            st.error(f"Ocurrió un error al cargar o procesar el archivo CSV: {e}")
            return None
    return None

# 3. Función para Definir Perfil del Stakeholder (Sin cambios importantes)
def obtener_perfil_stakeholder(tipo_stakeholder="gerente_produccion"):
    perfiles = {
        "gerente_produccion": {
            "nombre_display": "Gerente de Producción (Industria Porcina)", # Nuevo campo para la UI
            "objetivo": "comprender el desempeño financiero en relación con las operaciones de la granja, identificar áreas de mejora en costos operativos (especialmente alimento y salud animal) y eficiencia de producción.",
            "metricas_clave": [
                "Ingresos Totales", "Utilidad Bruta", "Costo Alimento",
                "Costo Salud Animal", "Costo Mano Obra", "FCR (Relación Conversión Alimento)",
                "Mortalidad (%)", "Cantidad Cerdos Vendidos", "Peso Promedio Venta (kg)"
            ],
            "tono": "analítico, enfocado en la acción, claro y directo, evitando jerga contable compleja.",
            "enfoque_narrativa": "Explica cómo las métricas operativas impactan los resultados financieros. Resalta los costos clave y la eficiencia. Sugiere áreas generales de enfoque para optimización.",
            "ejemplos_frases": "El costo de alimento por cerdo vendido es crucial. ¿Cómo estamos en FCR? La mortalidad impacta directamente la utilidad."
        },
        "inversor": { # ¡Añadimos un segundo perfil para demostrar la selección!
            "nombre_display": "Inversor General",
            "objetivo": "evaluar la rentabilidad general, el crecimiento, la salud financiera y los riesgos asociados con la inversión en la empresa.",
            "metricas_clave": [
                "Ingresos Totales", "Utilidad Bruta", "Utilidad Neta",
                "Margen Bruto (%)", "Margen Neto (%)", "Retorno sobre la Inversión (ROI)"
            ],
            "tono": "formal, enfocado en el retorno de la inversión, conciso y estratégico.",
            "enfoque_narrativa": "Resume los puntos clave de rendimiento financiero, el crecimiento y la sostenibilidad. Identifica los principales generadores de ingresos y costos, y aborda brevemente las perspectivas futuras.",
            "ejemplos_frases": "La rentabilidad ha mejorado este trimestre. Nuestro margen bruto es competitivo."
        }
    }
    return perfiles.get(tipo_stakeholder)

# 4. Función para Generar Prompt para el LLM (Sin cambios importantes)
def generar_prompt(datos, perfil):
    datos_relevantes = {k: v for k, v in datos.items() if k in perfil["metricas_clave"]}

    # Formateo de datos para el prompt
    formato_datos_prompt = []
    for k, v in datos_relevantes.items():
        if isinstance(v, (int, float)):
            if k in ["FCR (Relación Conversión Alimento)", "Mortalidad (%)"]:
                formato_datos_prompt.append(f"- {k}: {v}") # Porcentajes o FCR sin formato de miles
            else:
                formato_datos_prompt.append(f"- {k}: {v:,.0f}") # Números grandes con formato de miles
        else:
            formato_datos_prompt.append(f"- {k}: {v}")

    prompt = f"""
    Eres un analista financiero experto. Tu tarea es generar una narrativa concisa y clara de los resultados financieros y operativos para un **{perfil['nombre_display']}**.

    **Contexto de la Empresa:** {st.session_state.tipo_empresa_seleccionada}
    **Datos del Período:**
    {chr(10).join(formato_datos_prompt)}

    **Objetivo del Lector:** {perfil['objetivo']}
    **Métricas Clave a Resaltar:** {', '.join(perfil['metricas_clave'])}
    **Tono de la Narrativa:** {perfil['tono']}
    **Enfoque de la Narrativa:** {perfil['enfoque_narrativa']}

    Por favor, redacta un informe en lenguaje natural que sea fácil de entender, evitando la jerga contable excesiva. Concéntrate en las métricas clave y su impacto. La extensión debe ser de 3-5 párrafos.
    """
    return prompt

# 5. Función para Llamar al LLM y Obtener la Narrativa (Sin cambios importantes)
@st.cache_data(show_spinner="Generando narrativa, esto puede tardar unos segundos...") # Indicador de carga
def obtener_narrativa_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # O "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful and concise financial analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Ocurrió un error al comunicarse con el LLM: {e}. Revisa tu clave API o la conexión a internet.")
        return "No se pudo generar la narrativa."

# --- Interfaz de Usuario con Streamlit ---
st.set_page_config(page_title="Generador de Narrativas Financieras", layout="centered")

st.title("📊 Generador de Narrativas Financieras")
st.markdown("Carga tus datos contables y genera informes personalizados para diferentes stakeholders.")

# 1. Selector de Tipo de Empresa (simplificado para el MVP)
st.subheader("Paso 1: Selecciona el Tipo de Empresa")
tipo_empresa = st.selectbox(
    "Selecciona la industria:",
    ("Industria Porcina", "Laboratorio de Metrología", "Otro (Especificar)"), # Puedes expandir esto
    index=0
)
# Guardar en session_state para usarlo en el prompt
st.session_state.tipo_empresa_seleccionada = tipo_empresa

# 2. Carga de Archivo CSV
st.subheader("Paso 2: Carga tu Archivo de Datos CSV")
uploaded_file = st.file_uploader("Arrastra y suelta tu archivo CSV aquí, o haz clic para seleccionarlo.", type=["csv"])

datos_cargados = None
if uploaded_file is not None:
    datos_cargados = cargar_datos(uploaded_file)
    if datos_cargados:
        st.success("Archivo cargado exitosamente. Datos detectados:")
        st.write(pd.DataFrame.from_dict(datos_cargados, orient='index', columns=['Valor'])) # Muestra los datos

# 3. Selección del Stakeholder
st.subheader("Paso 3: Selecciona el Stakeholder")
# Mapeo para el selectbox
perfiles_disponibles = {
    "Gerente de Producción (Industria Porcina)": "gerente_produccion",
    "Inversor General": "inversor"
}
selected_stakeholder_display = st.selectbox(
    "¿Para quién es este informe?",
    list(perfiles_disponibles.keys()),
    index=0 # Default a Gerente de Producción
)
selected_stakeholder_key = perfiles_disponibles[selected_stakeholder_display]

perfil_target = obtener_perfil_stakeholder(selected_stakeholder_key)

# 4. Botón para Generar Narrativa
st.subheader("Paso 4: Generar Narrativa")
if st.button("Generar Informe Narrativo", type="primary"):
    if datos_cargados and perfil_target:
        with st.spinner('Procesando datos y generando narrativa...'):
            prompt_para_llm = generar_prompt(datos_cargados, perfil_target)
            narrativa_generada = obtener_narrativa_llm(prompt_para_llm)

            st.markdown("---")
            st.subheader(f"Informe Narrativo para el {perfil_target['nombre_display']}")
            st.write(narrativa_generada)
            st.success("Narrativa generada con éxito.")

            # Opción para copiar al portapapeles (requiere JavaScript, Streamlit no lo hace nativamente)
            # Como alternativa, se puede poner un botón que muestre un código para copiar
            st.download_button(
                label="Descargar Narrativa (TXT)",
                data=narrativa_generada,
                file_name=f"informe_narrativo_{selected_stakeholder_key}.txt",
                mime="text/plain"
            )
    elif not datos_cargados:
        st.warning("Por favor, carga un archivo CSV en el Paso 2 antes de generar el informe.")
    elif not perfil_target:
        st.error("No se pudo cargar el perfil del stakeholder.")

# Opcional: Sección de depuración para ver el prompt
if st.checkbox("Mostrar Prompt Generado (solo para depuración)"):
    if datos_cargados and perfil_target:
        st.text_area("Prompt enviado al LLM:", generar_prompt(datos_cargados, perfil_target), height=300)
    else:
        st.info("Carga datos y selecciona un stakeholder para ver el prompt.")
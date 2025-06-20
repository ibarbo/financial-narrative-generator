import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

# --- Configuración de OpenAI ---
# Usa st.secrets para producción o variables de entorno para desarrollo local
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) # Para Streamlit Cloud
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # Para desarrollo local

# --- Definición de Perfiles de Stakeholders ---
# Puedes mover esto a un archivo JSON externo si crece mucho
perfiles_stakeholders = {
    "gerente_produccion": {
        "nombre_display": "Gerente de Producción de Industria Porcina",
        "objetivo": "comprender el desempeño operativo y financiero directo de la granja, con enfoque en la eficiencia y los costos de producción.",
        "metricas_clave": [
            "Ingresos Totales", "Utilidad Bruta", "Costo Alimento", "Costo Salud Animal",
            "Costo Mano Obra", "Otros Costos Directos Produccion", "FCR (Relacion Conversion Alimento)",
            "Mortalidad (%)", "Cantidad Cerdos Vendidos", "Peso Promedio Venta (kg)",
            "Costo por Cerdo Vendido", "Precio Venta Promedio por Kg"
        ],
        "tono": "analítico, directo y enfocado en la eficiencia operativa.",
        "enfoque_narrativa": "abordar las métricas de producción y costos, explicando su impacto en la rentabilidad y sugiriendo áreas de optimización operativa.",
        "ejemplos_frases": "Nuestra eficiencia en alimento fue de X. ¿Cómo podemos reducir el costo por cerdo?"
    },
    "inversor_general": {
        "nombre_display": "Inversor General",
        "objetivo": "evaluar la salud financiera general de la empresa, la rentabilidad, el crecimiento y el riesgo de inversión.",
        "metricas_clave": [
            "Ingresos Totales", "Utilidad Neta del Periodo", "Margen Neto (%)",
            "Total Activos", "Total Pasivos", "Total Patrimonio", "Razon Corriente (Liquidez)",
            "Nivel de Endeudamiento (Pasivo/Activo)", "Crecimiento de Ingresos (vs periodo anterior si disponible)"
        ],
        "tono": "estratégico, transparente y enfocado en el potencial de retorno de inversión.",
        "enfoque_narrativa": "presentar un resumen de la rentabilidad, liquidez y solidez financiera, destacando los puntos fuertes y los riesgos.",
        "ejemplos_frases": "Nuestra rentabilidad neta es del X%. Los activos superan los pasivos por Y."
    },
    "gerente_general": {
        "nombre_display": "Gerente General / Dueño de la Granja",
        "objetivo": "comprender el desempeño financiero integral de la empresa (rentabilidad, liquidez, endeudamiento) y las áreas clave de impacto operacional.",
        "metricas_clave": [
            "Ingresos Totales", "Utilidad Bruta", "Utilidad Operacional", "Utilidad Neta del Periodo",
            "Costo Alimento", "Costo Salud Animal", "Activos No Corrientes Netos", "Total Activos",
            "Total Pasivos", "Total Patrimonio", "Efectivo y Equivalentes", "Cuentas por Cobrar Clientes",
            "Inventarios", "Proveedores", "Obligaciones Financieras Corto Plazo",
            "FCR (Relacion Conversion Alimento)", "Mortalidad (%)", "Margen Neto (%)",
            "Razon Corriente (Liquidez)", "Nivel de Endeudamiento (Pasivo/Activo)"
        ],
        "tono": "analítico, estratégico, transparente y directivo.",
        "enfoque_narrativa": "Ofrece una visión general del rendimiento, la salud financiera y los puntos clave que requieren atención o celebración. Balancea los resultados operativos con la situación financiera.",
        "ejemplos_frases": "Nuestra rentabilidad neta es X. La liquidez de la empresa es sólida. ¿Cómo afecta la deuda a nuestros planes de expansión?"
    },
    "personal_campo": {
        "nombre_display": "Personal de Campo",
        "objetivo": "comprender cómo su trabajo diario impacta las métricas clave de producción y los costos de la granja, presentado de forma muy sencilla y directa.",
        "metricas_clave": [
            "Ingresos Totales", "Costo Alimento", "Costo Salud Animal", "Cantidad Cerdos Vendidos",
            "FCR (Relacion Conversion Alimento)", "Mortalidad (%)", "Peso Promedio Venta (kg)"
        ],
        "tono": "sencillo, directo, motivador y cercano.",
        "enfoque_narrativa": "explicar el significado de las métricas de producción y costos de manera muy simple, destacando la importancia de su trabajo.",
        "ejemplos_frases": "Su trabajo en el día a día es clave. Así es como el alimento afecta las ganancias."
    }
}

# --- Funciones de la Aplicación ---

def generar_prompt(datos, perfil, tipo_empresa):
    datos_relevantes = {k: v for k, v in datos.items() if k in perfil["metricas_clave"]}

    # Formateo de datos para el prompt
    formato_datos_prompt = []
    for k, v in datos_relevantes.items():
        if isinstance(v, (int, float)):
            # Formato específico para porcentajes y ratios sin miles, y 1 o 2 decimales
            if "%" in k or "FCR" in k or "Razon Corriente" in k or "Nivel de Endeudamiento" in k:
                formato_datos_prompt.append(f"- {k}: {v:.2f}") # Dos decimales para porcentajes y ratios
            else:
                # Formato para números grandes con separador de miles
                formato_datos_prompt.append(f"- {k}: {v:,.0f}".replace(",", "_").replace(".", ",").replace("_", "."))
        else:
            formato_datos_prompt.append(f"- {k}: {v}")


    prompt = f"""
    Eres un **analista financiero senior y experto en la industria del sector {tipo_empresa}**. Tu objetivo es transformar los datos financieros y operativos en una **narrativa clara, concisa y procesable** para un **{perfil['nombre_display']}**.

    **Instrucciones Clave para la Generación de la Narrativa:**

    1.  **Audiencia:** Dirígete específicamente al "{perfil['nombre_display']}".
    2.  **Tono:** El tono debe ser {perfil['tono']}. Evita la jerga contable compleja; si usas un término técnico, explícalo brevemente de forma sencilla.
    3.  **Enfoque Principal:** La narrativa debe {perfil['enfoque_narrativa']}.
    4.  **Métricas Clave:** Incorpora y explica el significado de las siguientes métricas, que son las más relevantes para esta audiencia: {', '.join(perfil['metricas_clave'])}.
    5.  **Estructura:**
        * **Párrafo 1 (Resumen Ejecutivo):** Inicia con un resumen general del desempeño del período, destacando los ingresos y la utilidad bruta (o neta, según el perfil).
        * **Párrafo 2 (Análisis de Costos Clave / Situación Financiera):** Detalla los principales costos operativos, o para perfiles más estratégicos, los activos y pasivos clave. Explica su impacto.
        * **Párrafo 3 (Métricas Operativas / Ratios Financieros):** Enfócate en los indicadores de eficiencia (FCR, Mortalidad) o en los ratios de salud financiera (Liquidez, Endeudamiento), explicando su implicación.
        * **Párrafo 4 (Conclusiones y Recomendaciones/Áreas de Enfoque):** Ofrece una conclusión breve y, si aplica, sugerencias de áreas de enfoque sin ser prescriptivo (ej. "identificar oportunidades de mejora").
    6.  **Extensión:** La narrativa debe tener entre 4 y 5 párrafos.
    7.  **Precisión:** Asegúrate de que todos los datos numéricos mencionados sean exactamente los proporcionados. No inventes cifras ni tendencias que no estén implícitas en los datos. No incluyas información de periodos anteriores si no está explícitamente en los datos proporcionados.
    8.  **Formato:** Utiliza lenguaje natural, como si fuera escrito por un humano.

    **Datos Financieros y Operativos del Período Actual:**
    {chr(10).join(formato_datos_prompt)}

    Genera ahora la narrativa del informe.
    """
    return prompt

def limpiar_estado():
    """Reinicia el estado de la aplicación."""
    st.session_state.uploaded_file = None
    st.session_state.df_datos = None
    st.session_state.selected_stakeholder = None
    st.session_state.narrative_output = None
    st.session_state.tipo_empresa_seleccionada = "Porcina" # Reinicia al valor por defecto
    st.success("La aplicación ha sido reiniciada. Puedes cargar un nuevo archivo.")

# --- Configuración de la Interfaz de Usuario ---
st.set_page_config(
    page_title="Generador de Narrativas Financieras",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Generador de Narrativas Financieras (MVP)")
st.write("Transforma tus datos financieros y operativos en informes narrativos claros y personalizados con ayuda de la IA.")

# Inicializar estado de la sesión si no existe
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'df_datos' not in st.session_state:
    st.session_state.df_datos = None
if 'selected_stakeholder' not in st.session_state:
    st.session_state.selected_stakeholder = None
if 'narrative_output' not in st.session_state:
    st.session_state.narrative_output = None
if 'tipo_empresa_seleccionada' not in st.session_state:
    st.session_state.tipo_empresa_seleccionada = "Porcina" # Valor por defecto


# Botón "Limpiar" en la parte superior de la página principal
if st.button("Limpiar y Reiniciar la Aplicación", help="Borra todos los datos cargados y reinicia el proceso."):
    limpiar_estado()


# --- Sección de Carga de Datos ---
st.header("Paso 1: Carga tus Datos Financieros (CSV)")
st.write("Sube un archivo CSV con tus métricas financieras y operativas. Asegúrate de que tenga exactamente dos columnas: `metrica` y `valor`.")

uploaded_file = st.file_uploader("Arrastra y suelta tu archivo CSV aquí o haz clic para buscar", type="csv")

if uploaded_file is not None:
    if st.session_state.uploaded_file != uploaded_file: # Para evitar recargar si el archivo es el mismo
        st.session_state.uploaded_file = uploaded_file
        try:
            df = pd.read_csv(uploaded_file)
            if 'metrica' in df.columns and 'valor' in df.columns:
                st.session_state.df_datos = df
                st.success("¡Archivo CSV cargado con éxito! Filas: " + str(len(df)))
                st.dataframe(df.head()) # Muestra las primeras filas para confirmación
            else:
                st.session_state.df_datos = None
                st.error("Error: El archivo CSV debe contener las columnas 'metrica' y 'valor'.")
                st.markdown("**Verifica:** Que el nombre de las columnas sea `metrica` y `valor` exactamente, y que los números no tengan comas para los miles (ej. `1000000` en lugar de `1,000,000`).")
        except Exception as e:
            st.session_state.df_datos = None
            st.error(f"Ocurrió un error al cargar o procesar el archivo CSV: {e}. Por favor, verifica el formato.")
            st.markdown("**Consejo:** Asegúrate de que el archivo es un CSV válido y que no hay caracteres especiales inesperados.")
else:
    # Este bloque solo se ejecuta si no hay un archivo cargado actualmente
    # y si antes sí lo había (es decir, el usuario lo quitó o limpió)
    if st.session_state.uploaded_file is None and st.session_state.df_datos is not None:
        st.session_state.df_datos = None
        st.session_state.narrative_output = None
        st.session_state.selected_stakeholder = None
        st.info("Archivo CSV eliminado. Por favor, sube uno nuevo para empezar.")


# --- Sección de Configuración de la Narrativa ---
if st.session_state.df_datos is not None:
    st.header("Paso 2: Configura la Narrativa")

    st.session_state.tipo_empresa_seleccionada = st.text_input(
        "Nombre del Sector/Industria (ej. Porcina, Láctea, Retail):",
        value=st.session_state.tipo_empresa_seleccionada,
        help="Ayuda a la IA a contextualizar mejor la narrativa."
    )

    st.subheader("Paso 3: Selecciona el Tipo de Stakeholder")
    st.session_state.selected_stakeholder = st.selectbox(
        "¿Para quién es este informe?",
        options=[""] + list(perfiles_stakeholders.keys()),
        format_func=lambda x: perfiles_stakeholders[x]["nombre_display"] if x else "Selecciona un perfil..."
    )

    if st.session_state.selected_stakeholder:
        perfil_seleccionado = perfiles_stakeholders[st.session_state.selected_stakeholder]
        st.info(f"""
        **Perfil:** {perfil_seleccionado['nombre_display']}
        **Objetivo:** {perfil_seleccionado['objetivo']}
        **Tono Sugerido:** {perfil_seleccionado['tono']}
        """)
        st.write("Métricas clave que la IA intentará priorizar para este perfil:")
        st.code(", ".join(perfil_seleccionado['metricas_clave']))
    else:
        st.warning("Por favor, selecciona un perfil de stakeholder para continuar.")

    st.subheader("Paso 4: Generar Informe Narrativo")
    if st.button("Generar Informe"):
        if st.session_state.df_datos is not None and st.session_state.selected_stakeholder:
            try:
                perfil = perfiles_stakeholders[st.session_state.selected_stakeholder]
                datos_dict = st.session_state.df_datos.set_index('metrica')['valor'].to_dict()

                with st.spinner('Generando el informe... esto puede tardar unos segundos.'):
                    prompt_final = generar_prompt(datos_dict, perfil, st.session_state.tipo_empresa_seleccionada)
                    
                    # Llamada a la API de OpenAI
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo", # Modelo recomendado para MVP: costo-efectivo y buena calidad
                        messages=[
                            {"role": "system", "content": "You are a helpful and expert financial analyst assistant."},
                            {"role": "user", "content": prompt_final}
                        ],
                        temperature=0.4 # Mantener la creatividad baja para precisión financiera
                    )
                    st.session_state.narrative_output = response.choices[0].message.content
                    st.success("¡Informe generado con éxito! Aquí está la narrativa:")
            except Exception as e:
                st.session_state.narrative_output = None
                st.error(f"Ocurrió un error al generar la narrativa. Por favor, verifica tu clave API de OpenAI y los datos de entrada. Detalle: {e}")
                st.markdown("**Solución:** Revisa tu archivo CSV (columnas, formato numérico) y que tu clave API sea válida.")
        else:
            st.warning("Asegúrate de haber cargado un archivo CSV y seleccionado un perfil de stakeholder.")

# --- Sección de Visualización de la Narrativa ---
if st.session_state.narrative_output:
    st.header("Paso 5: Tu Informe Narrativo")
    st.markdown(st.session_state.narrative_output)

    # Botón "Limpiar" al final del informe para facilitar un nuevo ciclo
    st.write("---") # Separador visual
    if st.button("Generar Nuevo Informe / Reiniciar Aplicación", help="Haz clic aquí para borrar el informe actual y empezar un nuevo proceso."):
        limpiar_estado()
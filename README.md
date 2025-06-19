# 📊 Generador de Narrativas Financieras (MVP)

Este proyecto es un **Producto Mínimo Viable (MVP)** de una herramienta innovadora diseñada para transformar datos contables y operativos complejos en narrativas financieras claras y personalizadas, adaptadas para diferentes tipos de stakeholders (interesados). Su objetivo principal es resolver el desafío común de comunicar información financiera a audiencias no técnicas, como gerentes de producción, inversores o miembros de la junta directiva.

---

## 🌟 ¿Por qué este proyecto?

En el ámbito contable, es frecuente que los informes financieros, aunque precisos, sean difíciles de comprender para aquellos sin formación específica. Este MVP aborda esta brecha de comunicación, utilizando la inteligencia artificial (Modelos de Lenguaje Grandes - LLM) para generar textos explicativos que son relevantes y comprensibles para cada perfil de interesado, facilitando así una toma de decisiones más informada.

---

## 🚀 Características del MVP

* **Carga de Datos CSV:** Permite cargar archivos CSV simples con métricas financieras y operativas.
* **Perfiles de Stakeholders:** Incluye perfiles predefinidos (inicialmente para **Gerente de Producción de Industria Porcina** y **Inversor General**) para adaptar el tono y las métricas relevantes en la narrativa.
* **Generación de Narrativa con IA:** Utiliza la API de OpenAI (o similar) para redactar informes comprensibles.
* **Interfaz de Usuario Sencilla (Streamlit):** Una aplicación web interactiva y fácil de usar para cargar datos y generar informes con pocos clics.

---

## 🛠️ Tecnologías Utilizadas

* **Python:** Lenguaje de programación principal para la lógica del proyecto.
* **Pandas:** Para el procesamiento y manipulación de datos.
* **Streamlit:** Para construir la interfaz de usuario web interactiva.
* **OpenAI API:** Para acceder a los Modelos de Lenguaje Grandes (LLM) que generan las narrativas.
* **python-dotenv:** Para la gestión segura de las claves API.

---

## ⚙️ Configuración del Entorno de Desarrollo

Sigue estos pasos para poner en marcha el proyecto en tu máquina local:

1.  **Clona este Repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO_GITHUB/financial-narrative-generator.git](https://github.com/TU_USUARIO_GITHUB/financial-narrative-generator.git)
    cd financial-narrative-generator
    ```
    *(Nota: Reemplaza `TU_USUARIO_GITHUB` con tu nombre de usuario real en GitHub cuando hayas creado el repositorio.)*

2.  **Crea y Activa un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instala las Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    *(**Importante:** Primero necesitas crear el archivo `requirements.txt`. Ejecuta `pip freeze > requirements.txt` después de instalar todas las dependencias como `pandas`, `openai`, `streamlit`, `python-dotenv`.)*

4.  **Configura tu Clave API de OpenAI:**
    * Obtén tu clave API en [platform.openai.com](https://platform.openai.com/).
    * Crea un archivo llamado `.env` en la raíz de tu proyecto (al mismo nivel que `app.py`) y añade tu clave:
        ```
        OPENAI_API_KEY="tu_clave_api_aqui"
        ```
    * **¡Nunca subas este archivo `.env` a GitHub!** Se recomienda añadirlo a tu `.gitignore`.

---

## 🚀 Cómo Ejecutar el MVP

1.  **Prepara tus Datos:**
    * Crea un archivo CSV con tus datos financieros y operativos. Puedes usar `datos_porcinos.csv` o `datos_porcinos_variante.csv` como ejemplos. Asegúrate de que tenga una columna `metrica` y una columna `valor`.
        ```csv
        metrica,valor
        Ingresos Totales,50000000
        Costo Alimento,30000000
        ...
        ```

2.  **Inicia la Aplicación Streamlit:**
    ```bash
    streamlit run app.py
    ```

3.  **Interactúa con la Interfaz:**
    * Tu navegador web se abrirá automáticamente en `http://localhost:8501`.
    * Sube tu archivo CSV en la sección "Paso 2".
    * Selecciona el tipo de stakeholder en la sección "Paso 3".
    * Haz clic en "Generar Informe Narrativo" en el "Paso 4" para ver la magia.

---

## 📈 Futuras Mejoras (Roadmap del Producto)

Este MVP es solo el comienzo. Las futuras fases podrían incluir:

* Gestión dinámica de perfiles de stakeholders y plantillas de narrativa.
* Soporte para múltiples tipos de industrias y formatos de datos.
* Análisis de tendencias, comparativas inter-periodo y gráficos integrados.
* Integraciones con sistemas contables y ERPs.
* Funcionalidades de colaboración y exportación de informes.

---

## 🤝 Contribuciones

Este proyecto es de código abierto (en su fase de MVP). ¡Las contribuciones son bienvenidas! Si tienes ideas o mejoras, no dudes en abrir un *issue* o enviar un *pull request*.

---

## 📧 Contacto

Para preguntas o soporte, por favor contacta a [Tu Correo Electrónico o LinkedIn].
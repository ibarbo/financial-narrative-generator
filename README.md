# 📊 Financial Narrative Generator (MVP)

---

## 🚀 Overview

The **Financial Narrative Generator** is an innovative project designed to bridge the communication gap between complex financial data and non-technical stakeholders. It transforms raw accounting and operational figures into clear, concise, and personalized narratives using Artificial Intelligence.

This Minimum Viable Product (MVP) focuses on the **porcine industry** to demonstrate its core value proposition: making financial reports understandable for diverse audiences, such as farm production managers, general managers, investors, and even field personnel.

---

## ✨ Key Features (MVP)

* **CSV Data Ingestion**: Easily upload financial and operational data via a simple CSV file with `metrica` and `valor` columns.
* **Stakeholder-Specific Narratives**: Generate tailored reports based on the selected audience (e.g., Gerente de Producción, Inversor General, Gerente General/Dueño, Personal de Campo).
* **AI-Powered Explanations**: Utilizes OpenAI's language models (`gpt-3.5-turbo` for cost-efficiency) to translate numerical data into human-readable insights.
* **Intuitive User Interface**: Built with Streamlit for a simple, interactive web application experience.
* **Clear Feedback**: Provides success messages, clear error handling, and loading indicators for a smoother user experience.
* **Easy Reset**: A "Limpiar y Reiniciar" (Clear and Reset) button allows users to quickly prepare for a new report generation.

---

## 🎯 The Problem Solved

Traditional financial reports, while accurate, are often dense with jargon, codes, and numerical tables that are difficult for non-accountants to interpret. This leads to:
* Misunderstandings and confusion among stakeholders.
* Suboptimal decision-making due to unclear financial context.
* Increased workload for accountants who manually translate and explain reports for different audiences.

Our solution empowers accountants to deliver **impactful financial insights** effortlessly, fostering better understanding and more informed decisions across the organization.

---

## 🛠️ Technical Stack

* **Python**: The core programming language.
* **Streamlit**: For building the interactive web user interface.
* **Pandas**: For efficient data manipulation and processing of CSV files.
* **OpenAI API**: To access powerful Large Language Models (LLMs) for narrative generation.
* **`python-dotenv`**: For secure management of API keys and environment variables.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally:

### Prerequisites

* Python 3.8+ installed.
* An OpenAI API Key.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-username/financial-narrative-generator.git](https://github.com/your-username/financial-narrative-generator.git)
    cd financial-narrative-generator
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to create a `requirements.txt` file by running `pip freeze > requirements.txt` after installing `streamlit`, `pandas`, `openai`, `python-dotenv` if it's not already present)*.

4.  **Set up your OpenAI API Key**:
    * Create a file named `.env` in the root directory of your project.
    * Add your OpenAI API key to this file:
        ```
        OPENAI_API_KEY="your_openai_api_key_here"
        ```
        **Never commit your `.env` file to version control.** Make sure it's included in your `.gitignore`.

### Running the Application

1.  **Start the Streamlit application**:
    ```bash
    streamlit run app.py
    ```
2.  Your browser will automatically open a new tab with the Streamlit application (usually at `http://localhost:8501`).

---

## 🧪 How to Use

1.  **Prepare your data**: Ensure your CSV file has exactly two columns: `metrica` and `valor`. For numerical values, remove any thousand separators (e.g., `1000000` instead of `1,000,000`).
    * You can use the provided example file: `datos_financieros_completo_formateado.csv`
2.  **Upload the CSV**: Click on the file uploader in the Streamlit app to select your CSV.
3.  **Specify Industry**: Enter the industry relevant to your data (e.g., "Porcina").
4.  **Select Stakeholder Profile**: Choose the audience for whom you want to generate the report (e.g., "Gerente de Producción", "Inversor General").
5.  **Generate Report**: Click the "Generar Informe" button. The AI will process the data and display the narrative.
6.  **Review and Reset**: Read the generated narrative. Use the "Limpiar y Reiniciar la Aplicación" button to clear the current session and start a new report.

---

## 🛣️ Future Enhancements (Roadmap)

This MVP is just the beginning. Our vision includes:

* **Advanced Data Ingestion**: Handling more complex CSV formats directly, reducing manual pre-processing.
* **Custom Stakeholder Profiles**: Allowing users to define and save their own stakeholder profiles and reporting preferences.
* **Interactive Q&A**: Enabling users to ask natural language questions about their financial data.
* **Text-to-Speech (TTS)**: Integrating audio generation so users can listen to their reports.
* **Visualizations**: Generating simple charts and graphs within the interface to complement the narratives.
* **Presentation Integration**: Facilitating the export of key insights for presentation slides.

---

## 🤝 Contribution & Feedback

We welcome your feedback and suggestions! This project is being developed collaboratively to build a valuable solution for accountants and businesses.

---
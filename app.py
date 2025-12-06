"""
app.py
Streamlit App para Detección de Plagio

Autores: Alma Paulina González Sandoval, Diego Sánchez Valle
Fecha: Diciembre 2025

Aplicación web para comparar dos documentos y detectar plagio.
"""

import streamlit as st
import sys
import os
import tempfile
import plotly.graph_objects as go
import plotly.express as px

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.plagiarism_detector import PlagiarismDetector


@st.cache_resource
def load_plagiarism_detector(language, model_name='paraphrase-multilingual-MiniLM-L12-v2'):
    """
    Cachea el detector para evitar recargarlo en cada interacción.
    Esto mejora significativamente el rendimiento en deployment.
    """
    return PlagiarismDetector(language=language, model_name=model_name)


def create_gauge_chart(percentage, title):
    """Crea un gráfico de gauge para mostrar el porcentaje"""

    # Determinar color basado en el porcentaje
    if percentage >= 75:
        color = "red"
    elif percentage >= 50:
        color = "orange"
    elif percentage >= 30:
        color = "yellow"
    else:
        color = "green"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 50], 'color': "lightyellow"},
                {'range': [50, 75], 'color': "lightcoral"},
                {'range': [75, 100], 'color': "lightpink"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 75
            }
        }
    ))

    fig.update_layout(height=300)
    return fig


def create_breakdown_chart(breakdown_data):
    """Crea un gráfico de barras para el desglose de métricas"""

    categories = list(breakdown_data.keys())
    values = [float(v.strip('%')) for v in breakdown_data.values()]
    text_labels = list(breakdown_data.values())

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
            text=text_labels,
            textposition='auto',
        )
    ])

    fig.update_layout(
        title="Desglose por Categorías de Análisis",
        xaxis_title="Categoría",
        yaxis_title="Similitud (%)",
        yaxis_range=[0, 100],
        height=400
    )

    return fig


def get_verdict_color(similarity_percentage):
    """Retorna el color basado en el nivel de similitud"""
    if similarity_percentage >= 75:
        return "red"
    elif similarity_percentage >= 50:
        return "orange"
    elif similarity_percentage >= 30:
        return "yellow"
    else:
        return "green"


def main():
    st.set_page_config(
        page_title="Detector de Plagio",
        page_icon="📝",
        layout="wide"
    )

    st.title("📝 Detector de Plagio con Análisis Multidimensional")
    st.markdown("---")

    # Sidebar con información
    with st.sidebar:
        st.header("⚙️ Configuración")

        language = st.selectbox(
            "Idioma del texto",
            options=["spanish", "english"],
            index=0
        )

        st.markdown("---")
        st.header("📊 Información del Sistema")
        st.markdown("""
        Este detector utiliza **4 dimensiones de análisis**:

        - **Semántico (40%)**: Detecta parafraseo usando embeddings de BERT
        - **Léxico (30%)**: Analiza similitud de palabras y n-gramas
        - **Estructural (20%)**: Compara organización del documento
        - **Secuencia (10%)**: Detecta orden similar de ideas
        """)

        st.markdown("---")
        st.header("🎯 Interpretación")
        st.markdown("""
        - **90-100%**: Plagio casi seguro
        - **75-90%**: Plagio muy probable
        - **50-75%**: Plagio probable
        - **30-50%**: Similitud sospechosa
        - **0-30%**: Similitud baja (original)
        """)

        st.markdown("---")
        st.markdown("**Autores:**")
        st.markdown("Alma Paulina González Sandoval")
        st.markdown("Diego Sánchez Valle")

    # Área principal
    st.header("📄 Cargar Documentos para Comparar")

    # Variables para almacenar los textos de los archivos
    file1_text = None
    file2_text = None

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Documento A")
        file1 = st.file_uploader(
            "Selecciona el primer archivo",
            type=['txt', 'md', 'pdf'],
            key="file1"
        )

        if file1:
            file1_text = file1.read().decode('utf-8', errors='ignore')
            preview_text = file1_text[:500] + "..." if len(file1_text) > 500 else file1_text
            st.text_area("Vista previa - Documento A", preview_text, height=200, disabled=True)
            st.info(f"📊 Caracteres: {len(file1_text)} | Palabras: {len(file1_text.split())}")

    with col2:
        st.subheader("Documento B")
        file2 = st.file_uploader(
            "Selecciona el segundo archivo",
            type=['txt', 'md', 'pdf'],
            key="file2"
        )

        if file2:
            file2_text = file2.read().decode('utf-8', errors='ignore')
            preview_text = file2_text[:500] + "..." if len(file2_text) > 500 else file2_text
            st.text_area("Vista previa - Documento B", preview_text, height=200, disabled=True)
            st.info(f"📊 Caracteres: {len(file2_text)} | Palabras: {len(file2_text.split())}")

    st.markdown("---")

    # Sección de entrada de texto alternativa
    st.subheader("✍️ O escribe/pega texto directamente")

    col_text1, col_text2 = st.columns(2)

    with col_text1:
        direct_text1 = st.text_area(
            "Texto A",
            height=200,
            placeholder="Pega aquí el primer texto...",
            key="direct_text1"
        )

    with col_text2:
        direct_text2 = st.text_area(
            "Texto B",
            height=200,
            placeholder="Pega aquí el segundo texto...",
            key="direct_text2"
        )

    # Botón de comparación
    st.markdown("---")

    if st.button("🔍 Comparar Documentos", type="primary", use_container_width=True):
        # Determinar qué textos usar (prioridad: archivos > texto directo)
        text_a = None
        text_b = None

        # Primero intentar usar archivos cargados
        if file1_text and file2_text:
            text_a = file1_text
            text_b = file2_text
        # Si no hay archivos, usar texto directo
        elif direct_text1 and direct_text2:
            text_a = direct_text1
            text_b = direct_text2
        # Si hay un archivo y un texto, usar esa combinación
        elif file1_text and direct_text2:
            text_a = file1_text
            text_b = direct_text2
        elif direct_text1 and file2_text:
            text_a = direct_text1
            text_b = file2_text
        else:
            st.error("⚠️ Por favor proporciona dos textos para comparar (ya sea mediante archivos o escribiendo directamente).")
            st.stop()

        # Validar que ambos textos tengan contenido
        if not text_a or not text_a.strip():
            st.error("⚠️ El texto A está vacío.")
            st.stop()

        if not text_b or not text_b.strip():
            st.error("⚠️ El texto B está vacío.")
            st.stop()

        # Mostrar spinner mientras se procesa
        with st.spinner("🔄 Analizando documentos... Esto puede tomar unos segundos."):
            try:
                # Inicializar detector (cacheado para mejor rendimiento)
                detector = load_plagiarism_detector(language=language)

                # Comparar textos
                result = detector.compare_texts(text_a, text_b)

                # Mostrar resultados
                st.markdown("---")
                st.header("📊 Resultados del Análisis")

                # Resultado principal
                similarity = result['similarity_percentage']
                verdict = result['verdict']
                verdict_color = get_verdict_color(similarity)

                # Gauge principal
                st.plotly_chart(
                    create_gauge_chart(similarity, "Similitud Total"),
                    use_container_width=True
                )

                # Veredicto con color
                st.markdown(f"### Veredicto: :{verdict_color}[{verdict}]")

                st.markdown("---")

                # Desglose por categorías
                st.subheader("📈 Desglose Detallado por Categorías")

                # Gráfico de barras
                st.plotly_chart(
                    create_breakdown_chart(result['breakdown']),
                    use_container_width=True
                )

                # Tabla con métricas
                col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)

                with col_metrics1:
                    st.metric(
                        label="🧠 Semántico",
                        value=result['breakdown']['semantic'],
                        delta=None
                    )

                with col_metrics2:
                    st.metric(
                        label="📝 Léxico",
                        value=result['breakdown']['lexical'],
                        delta=None
                    )

                with col_metrics3:
                    st.metric(
                        label="🏗️ Estructural",
                        value=result['breakdown']['structural'],
                        delta=None
                    )

                with col_metrics4:
                    st.metric(
                        label="🔄 Secuencia",
                        value=result['breakdown']['sequence'],
                        delta=None
                    )

                st.markdown("---")

                # Información detallada en expandibles
                with st.expander("🔬 Análisis Semántico Detallado"):
                    semantic = result['details']['semantic']
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Similitud Global", f"{semantic['overall']*100:.2f}%")
                    with col2:
                        st.metric("Promedio de Oraciones", f"{semantic['sentence_avg']*100:.2f}%")
                    with col3:
                        st.metric("Oraciones Coincidentes", semantic['matched_sentences'])

                    st.info("El análisis semántico usa embeddings de BERT para detectar parafraseo y similitud de significado.")

                with st.expander("📖 Métricas Léxicas Detalladas"):
                    lexical = result['details']['lexical']
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("TF-IDF Coseno", f"{lexical['tfidf_cosine']*100:.2f}%")
                        st.metric("Jaccard", f"{lexical['jaccard']*100:.2f}%")

                    with col2:
                        st.metric("Trigramas", f"{lexical['trigram']*100:.2f}%")
                        st.metric("Dice Coefficient", f"{lexical['dice']*100:.2f}%")

                    st.info("Las métricas léxicas analizan similitud a nivel de palabras, n-gramas y vocabulario.")

                with st.expander("⚖️ Pesos Utilizados en el Análisis"):
                    weights = result['weights_used']

                    weights_data = {
                        'Categoría': list(weights.keys()),
                        'Peso': [f"{v*100:.0f}%" for v in weights.values()]
                    }

                    st.table(weights_data)
                    st.info("El puntaje final es una combinación ponderada de todas las métricas.")

                # Mensaje final según el resultado
                st.markdown("---")

                if similarity >= 75:
                    st.error("⚠️ **ALERTA**: Se ha detectado un nivel muy alto de similitud. Se recomienda una revisión manual inmediata.")
                elif similarity >= 50:
                    st.warning("⚠️ **ATENCIÓN**: Se ha detectado similitud considerable. Se recomienda revisar manualmente.")
                elif similarity >= 30:
                    st.warning("ℹ️ **NOTA**: Hay similitud moderada. Puede requerir revisión según el contexto.")
                else:
                    st.success("✅ **OK**: Los documentos muestran baja similitud y parecen ser originales.")

            except Exception as e:
                st.error(f"❌ Error durante el análisis: {str(e)}")
                st.exception(e)


if __name__ == "__main__":
    main()

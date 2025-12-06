# Streamlit App - Detector de Plagio

Aplicación web interactiva para comparar documentos y detectar plagio usando análisis multidimensional.

## Instalación

```bash
# Instalar dependencias (incluyendo streamlit)
pip install -r requirements.txt

# Descargar modelos de lenguaje
python -m spacy download es_core_news_md  # Español
python -m spacy download en_core_web_md   # Inglés (opcional)
```

## Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## Características

### 🎯 Funcionalidades Principales

1. **Carga de Archivos**: Sube dos archivos (.txt, .md, .pdf) para comparar
2. **Entrada Directa**: O escribe/pega texto directamente en la interfaz
3. **Análisis Multidimensional**: 4 dimensiones de análisis (Semántico, Léxico, Estructural, Secuencia)
4. **Visualizaciones Interactivas**:
   - Gauge chart con el porcentaje de similitud total
   - Gráfico de barras con desglose por categorías
   - Métricas detalladas expandibles
5. **Soporte Multiidioma**: Español e inglés

### 📊 Visualizaciones

- **Gauge Chart**: Muestra el porcentaje total de similitud con colores según el nivel de riesgo
  - Verde (0-30%): Original
  - Amarillo (30-50%): Sospechoso
  - Naranja (50-75%): Plagio probable
  - Rojo (75-100%): Plagio muy probable

- **Gráfico de Barras**: Desglose detallado de las 4 categorías de análisis

- **Métricas Expandibles**: Análisis detallado de cada dimensión

### 🎨 Interfaz

- **Sidebar**: Configuración de idioma e información del sistema
- **Área Principal**: Carga de documentos y visualización de resultados
- **Layout Responsivo**: Diseño en columnas para mejor visualización

## Uso

1. **Selecciona el idioma** en el sidebar (español o inglés)

2. **Carga los documentos**:
   - Opción A: Sube dos archivos usando los botones de carga
   - Opción B: Escribe/pega texto directamente en las cajas de texto

3. **Haz clic en "🔍 Comparar Documentos"**

4. **Revisa los resultados**:
   - Similitud total (gauge chart)
   - Veredicto con código de color
   - Desglose por categorías
   - Métricas detalladas (expandibles)

## Interpretación de Resultados

| Porcentaje | Color | Veredicto | Acción |
|-----------|-------|-----------|--------|
| 90-100% | Rojo | Plagio casi seguro | Revisión inmediata |
| 75-90% | Rojo | Plagio muy probable | Revisión inmediata |
| 50-75% | Naranja | Plagio probable | Revisar manualmente |
| 30-50% | Amarillo | Similitud sospechosa | Puede requerir revisión |
| 0-30% | Verde | Similitud baja | Probablemente original |

## Ejemplos de Uso

### Caso 1: Comparar dos ensayos
1. Sube `ensayo_estudiante.txt` y `ensayo_referencia.txt`
2. Selecciona idioma: español
3. Haz clic en comparar
4. Revisa el análisis semántico para detectar parafraseo

### Caso 2: Verificar texto pegado
1. Copia texto del documento A en la caja de texto A
2. Copia texto del documento B en la caja de texto B
3. Compara directamente sin subir archivos

## Tecnologías Utilizadas

- **Streamlit**: Framework de aplicación web
- **Plotly**: Visualizaciones interactivas
- **Sentence-BERT**: Análisis semántico
- **scikit-learn**: Métricas léxicas
- **NLTK**: Procesamiento de lenguaje natural

## Autores

- Alma Paulina González Sandoval
- Diego Sánchez Valle

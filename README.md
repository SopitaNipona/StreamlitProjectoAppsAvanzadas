# Detector de Plagio con Análisis Multidimensional

**Autores:** Alma Paulina González Sandoval, Diego Sánchez Valle

Sistema de detección de plagio que combina análisis semántico, léxico, estructural y de secuencias para determinar la similitud entre documentos de texto.

## Características Principales

### Análisis Multi-Dimensional

- **Análisis Semántico (40%)**: Utiliza Sentence-BERT para capturar el significado profundo del texto, detectando parafraseo sofisticado
- **Análisis Léxico (30%)**: Evalúa similitud a nivel de palabras, n-gramas, TF-IDF y vocabulario compartido
- **Análisis Estructural (20%)**: Considera longitud, organización, diversidad léxica y estilo del documento
- **Análisis de Secuencia (10%)**: Detecta orden similar de ideas mediante LCS y SequenceMatcher

### Instalación Manual

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Descargar modelos de lenguaje
python -m spacy download es_core_news_md  # Para español
python -m spacy download en_core_web_md   # Para inglés (opcional)

# 3. Probar el sistema
python test_simple.py
```

## 💡 Uso Básico

### Comparar dos textos

```python
from src.plagiarism_detector import PlagiarismDetector

# Inicializar detector
detector = PlagiarismDetector(language='spanish')

# Tus textos
texto_a = "La inteligencia artificial está revolucionando el mundo..."
texto_b = "La IA está transformando nuestro mundo de manera significativa..."

# Comparar
resultado = detector.compare_texts(texto_a, texto_b)

# Mostrar resultado
print(f"Similitud: {resultado['similarity_percentage']:.2f}%")
print(f"Veredicto: {resultado['verdict']}")

# Reporte completo
detector.print_report(resultado)
```

### Comparar dos archivos

```python
from src.plagiarism_detector import PlagiarismDetector

detector = PlagiarismDetector(language='spanish')

# Comparar archivos
resultado = detector.compare_files('documento_A.txt', 'documento_B.txt')
detector.print_report(resultado)
```

### Desde línea de comandos

```bash
cd examples
python quick_comparison.py archivo1.txt archivo2.txt
```

## 📊 Ejemplo de Salida

```
======================================================================
REPORTE DE ANÁLISIS DE SIMILITUD/PLAGIO
======================================================================

📄 Archivo A: documento_original.txt
📄 Archivo B: documento_sospechoso.txt

🎯 SIMILITUD TOTAL: 73.45%
📊 VEREDICTO: PLAGIO PROBABLE - Similitud significativa detectada

----------------------------------------------------------------------
DESGLOSE POR CATEGORÍAS:
----------------------------------------------------------------------
  • Semantic      : 78.32%
  • Lexical       : 65.12%
  • Structural    : 82.45%
  • Sequence      : 58.91%

----------------------------------------------------------------------
PESOS UTILIZADOS:
----------------------------------------------------------------------
  • Semantic      : 40.00%
  • Lexical       : 30.00%
  • Structural    : 20.00%
  • Sequence      : 10.00%

======================================================================
```

## 🎯 Interpretación de Resultados

| Porcentaje | Veredicto | Descripción |
|-----------|-----------|-------------|
| 90-100% | Plagio casi seguro | Textos idénticos o prácticamente iguales |
| 75-90% | Plagio muy probable | Parafraseo ligero, copia sustancial |
| 50-75% | Plagio probable | Parafraseo moderado, similitud significativa |
| 30-50% | Similitud sospechosa | Requiere revisión manual |
| 0-30% | Similitud baja | Textos probablemente originales |


## 🔬 Metodología Técnica

### Análisis Semántico (40%)
- **Modelo**: Sentence-BERT (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Técnica**: Embeddings de 384 dimensiones con similitud coseno
- **Ventaja**: Detecta parafraseo y reformulación de ideas

### Análisis Léxico (30%)
- **Métricas**: TF-IDF, Jaccard, Dice, N-gramas (2, 3, 4)
- **Técnica**: Comparación de vocabulario y secuencias de palabras
- **Ventaja**: Identifica copia literal y similitud superficial

### Análisis Estructural (20%)
- **Características**: Longitud, densidad, diversidad léxica
- **Técnica**: Comparación de propiedades estadísticas
- **Ventaja**: Detecta similitud en estilo y organización

### Análisis de Secuencia (10%)
- **Métricas**: LCS, SequenceMatcher
- **Técnica**: Búsqueda de subsecuencias comunes
- **Ventaja**: Detecta orden similar de ideas

## Casos de Uso

- **Academia**: Detección de plagio en ensayos, tesis y trabajos de investigación

## Documentación

- **[Manual_usuario.md](Manual_usuario.md)** - Manual de usuario
- **[TECHNICAL.md](TECHNICAL.md)** - Detalles técnicos y algoritmos

## Entrenamiento Personalizado

```bash
# 1. Generar dataset sintético
cd examples
python generate_dataset.py

# 2. Entrenar con tus datos
python train_model.py

# El sistema optimizará automáticamente pesos y umbrales
```

## Dependencias Principales

- `sentence-transformers` - Embeddings semánticos
- `transformers` - Modelos de lenguaje
- `torch` - Backend ML
- `scikit-learn` - Métricas y vectorización
- `nltk` - Procesamiento de lenguaje natural
- `spacy` - NLP avanzado

## Ejemplos 

Ejecuta los ejemplos para ver el sistema en acción:

```bash
cd examples
python compare_texts.py
```

Este script incluye 6 ejemplos demostrativos:
1. Textos idénticos (100% similitud)
2. Parafraseo (plagio semántico ~70-80%)
3. Textos diferentes (<30% similitud)
4. Plagio parcial (50-70%)
5. Comparación de archivos
6. Textos en inglés


### Ajustar pesos de métricas

```python
custom_weights = {
    'semantic': 0.50,    # Más peso a semántica
    'lexical': 0.25,
    'structural': 0.15,
    'sequence': 0.10,
}

detector = PlagiarismDetector(custom_weights=custom_weights)
```

### Cambiar modelo de embeddings

```python
# Más rápido (menos preciso)
detector = PlagiarismDetector(model_name='paraphrase-MiniLM-L6-v2')

# Más preciso (más lento)
detector = PlagiarismDetector(model_name='paraphrase-multilingual-mpnet-base-v2')
```


## Licencia

Este proyecto utiliza componentes con las siguientes licencias:
- Sentence-BERT: Apache License 2.0
- spaCy: MIT License
- NLTK: Apache License 2.0
- scikit-learn: BSD License


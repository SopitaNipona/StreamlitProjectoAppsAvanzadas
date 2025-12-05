# Guía de Uso - Detector de Plagio y Similitud de Textos

## Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Descargar modelos de lenguaje

```bash
# Para español
python -m spacy download es_core_news_md

# Para inglés
python -m spacy download en_core_web_md

# Descargar datos de NLTK
```
## Uso Básico

### Comparar dos textos directamente

```python
from src.plagiarism_detector import PlagiarismDetector

# Inicializar detector
detector = PlagiarismDetector(language='spanish')

# Definir textos
texto_a = "Tu primer texto aquí"
texto_b = "Tu segundo texto aquí"

# Comparar
resultado = detector.compare_texts(texto_a, texto_b)

# Imprimimr Resultado
detector.print_report(resultado)

# Acceder a datos específicos
print(f"Similitud: {resultado['similarity_percentage']:.2f}%")
print(f"Resultado: {resultado['verdict']}")
```

### Comparar archivos

```python
from src.plagiarism_detector import PlagiarismDetector

detector = PlagiarismDetector(language='spanish')

# Comparar dos archivos
resultado = detector.compare_files('documento_A.txt', 'documento_B.txt')
detector.print_report(resultado)
```

### Uso desde línea de comandos

```bash
# Comparación rápida
cd examples
python quick_comparison.py archivo1.txt archivo2.txt
```

## Ejemplos Completos

### Ejecutar demos

```bash
cd examples
python compare_texts.py
```

Esto ejecutará varios ejemplos que demuestran:
- Textos idénticos (100% similitud)
- Textos parafraseados (plagio semántico)
- Textos diferentes (baja similitud)
- Plagio parcial
- Comparación de archivos
- Textos en inglés

## Entrenamiento del Modelo

### 1. Generar dataset sintético

```bash
cd examples
python generate_dataset.py
```

Este script genera un dataset de 200 pares de textos con etiquetas de plagio/no plagio.

### 2. Entrenar el modelo

```python
from src.model_trainer import PlagiarismModelTrainer
from src.plagiarism_detector import PlagiarismDetector

# Crear detector
detector = PlagiarismDetector(language='spanish')

# Crear entrenador
trainer = PlagiarismModelTrainer(detector)

# Entrenar (optimiza pesos y umbrales)
results = trainer.train(
    dataset_path='data/training/plagiarism_dataset.csv',
    optimize_weights=True,
    optimize_threshold=True,
    test_size=0.2
)

# Guardar configuración optimizada
trainer.save_model_config('models/optimized_config.json', results)
```

### 3. Usar modelo entrenado

```python
from src.model_trainer import PlagiarismModelTrainer
from src.plagiarism_detector import PlagiarismDetector

# Crear detector
detector = PlagiarismDetector(language='spanish')

# Cargar configuración entrenada
trainer = PlagiarismModelTrainer(detector)
trainer.load_model_config('models/optimized_config.json')

# Ahora el detector usa los pesos optimizados
resultado = detector.compare_texts(texto_a, texto_b)
```

## Personalización

### Cambiar pesos de las métricas

```python
# Pesos personalizados (deben sumar 1)
custom_weights = {
    'semantic': 0.50,     # Más peso a similitud semántica
    'lexical': 0.25,      # Menos peso a léxico
    'structural': 0.15,   # Menos peso a estructura
    'sequence': 0.10,     # Mantener secuencia
}

detector = PlagiarismDetector(
    language='spanish',
    custom_weights=custom_weights
)
```

### Cambiar modelo de embeddings

```python
# Usar un modelo más grande (más preciso pero más lento)
detector = PlagiarismDetector(
    language='spanish',
    model_name='paraphrase-multilingual-mpnet-base-v2'
)

### Ajustar umbrales de detección

```python
detector = PlagiarismDetector(language='spanish')

# Modificar umbrales
detector.thresholds = {
    'high_plagiarism': 0.80,     
    'moderate_plagiarism': 0.60,  
    'low_plagiarism': 0.40,      
}
```

## Interpretación de Resultados

### Scores de Similitud

- **90-100%**: Plagio casi seguro (textos idénticos o muy similares)
- **75-90%**: Plagio muy probable (parafraseo ligero)
- **50-75%**: Plagio probable (parafraseo moderado)
- **30-50%**: Similitud sospechosa (requiere revisión)
- **0-30%**: Similitud baja (probablemente original)

### Desglose por categorías

El sistema analiza 4 dimensiones:

1. **Semántica (40% por defecto)**: Significado del texto usando embeddings
   - Captura parafraseo y reformulación de ideas
   - Más robusto ante cambios superficiales

2. **Léxica (30% por defecto)**: Palabras y n-gramas compartidos
   - Detecta copia literal de palabras
   - Útil para plagio directo

3. **Estructural (20% por defecto)**: Organización del texto
   - Longitud, número de párrafos, estilo
   - Complementa otras métricas

4. **Secuencia (10% por defecto)**: Orden de las ideas
   - Detecta si las ideas siguen el mismo orden
   - Útil para plagio con reordenamiento

## Datasets Personalizados

### Formato del CSV

```csv
text1,text2,is_plagiarism
"Texto original...","Texto plagiado...","True"
"Texto A...","Texto diferente...","False"
```

Columnas requeridas:
- `text1`: Primer texto
- `text2`: Segundo texto
- `is_plagiarism`: True/False (etiqueta)

### Crear dataset propio

```python
import pandas as pd

data = [
    {
        'text1': "Texto original 1",
        'text2': "Texto plagiado 1",
        'is_plagiarism': True
    },
    {
        'text1': "Texto original 2",
        'text2': "Texto diferente",
        'is_plagiarism': False
    },
    # ... más ejemplos
]

df = pd.DataFrame(data)
df.to_csv('data/training/my_dataset.csv', index=False)
```

## Mejores Prácticas

### Para mejor precisión:

1. **Usa textos largos**: El modelo funciona mejor con al menos 3-4 oraciones
2. **Limpia el texto**: Elimina encabezados, pies de página, metadatos
3. **Idioma consistente**: Usa el mismo idioma en ambos textos
4. **Entrena con datos reales**: Genera un dataset representativo de tu dominio
5. **Ajusta pesos**: Experimenta con diferentes pesos según tu caso de uso

### Para textos específicos:

- **Académicos**: Aumentar peso semántico (detecta parafraseo)
- **Noticias**: Aumentar peso léxico (copia literal)
- **Ensayos**: funciona bien balance estandar

## Solución de Problemas

### Error: "No module named 'sentence_transformers'"

```bash
pip install sentence-transformers
```

### Error al descargar modelo de embeddings

```python
# Especifica un modelo más pequeño
detector = PlagiarismDetector(
    model_name='paraphrase-MiniLM-L6-v2'
)
```

### Proceso muy lento

```python
# Usa modelo más ligero
detector = PlagiarismDetector(
    model_name='paraphrase-MiniLM-L6-v2'  # Más rápido
)
```

### Memoria insuficiente

- Usa modelos más pequeños
- Procesa textos en lotes más pequeños
- Reduce el tamaño del dataset de entrenamiento

## API Reference

Ver documentación en el código fuente de cada módulo:
- [plagiarism_detector.py](src/plagiarism_detector.py)
- [similarity_metrics.py](src/similarity_metrics.py)
- [text_preprocessor.py](src/text_preprocessor.py)
- [model_trainer.py](src/model_trainer.py)

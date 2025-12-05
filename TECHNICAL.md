# Metodología de Detección

## 1. Análisis Semántico - 40% weight

Técnica: Embeddings de oraciones usando Sentence-BERT

Modelo: `paraphrase-multilingual-MiniLM-L12-v2`
-Pre-entrenado en 50+ idiomas
-Dimensión de embeddings: 384
-Optimizado para similitud de paráfrasis

Proceso:

```python
embedding_A = model.encode(texto_A)
embedding_B = model.encode(texto_B)
similitud = cosine_similarity(embedding_A, embedding_B)

for sentence_A in sentences_A:
    best_match = max(cosine_similarity(sentence_A, sent_B)
                     for sent_B in sentences_B)
```

Ventajas:

- Detecta parafraseo sofisticado
- Captura significado contextual
- Robusto ante cambios de vocabulario

Cosas a mejorar:
- Requiere de un modelo pre-entrenado de gran volumen

## 2. Análisis Léxico - 30% weight

Métricas:

a. TF-IDF + Similitud Coseno

TF-IDF(palabra, documento) = TF(palabra) × IDF(palabra)
cosine_sim = (A · B) / (||A|| × ||B||)


b. Similitud de Jaccard

Jaccard(A, B) = |A ∩ B| / |A ∪ B|

c. N-gramas (bigrams, trigrams, 4-grams)

ngram_sim = |ngramas_A ∩ ngramas_B| / |ngramas_A ∪ ngramas_B|


d. Coeficiente de Dice

Dice(A, B) = 2 × |A ∩ B| / (|A| + |B|)


Score léxico final:

lexical_score = mean([
    tfidf_cosine,
    jaccard_words,
    trigram_similarity,
    dice_coefficient
])


## 3. Análisis Estructural - 20% weight

Características evaluadas:

features = {
    'char_count': len(text),
    'word_count': num_words,
    'sentence_count': num_sentences,
    'avg_word_length': mean_word_length,
    'avg_sentence_length': words_per_sentence,
    'lexical_diversity': unique_words / total_words
}

Similitud estructural:

structural_sim = mean([
    1 - |words_A - words_B| / max(words_A, words_B),
    1 - |sentences_A - sentences_B| / max(sentences_A, sentences_B),
    1 - |avg_word_len_A - avg_word_len_B| / max(...),
    1 - |avg_sent_len_A - avg_sent_len_B| / max(...),
    1 - |lex_div_A - lex_div_B|
])


## 4. Análisis de Secuencia - 10% weight

Técnicas:

a. SequenceMatcher (algoritmo de Ratcliff-Obershelp)

from difflib import SequenceMatcher
ratio = SequenceMatcher(None, text_A, text_B).ratio()


b. Longest Common Subsequence (LCS)

Programación dinámica
L[i][j] = L[i-1][j-1] + 1  si text1[i] == text2[j]
        = max(L[i-1][j], L[i][j-1])  en otro caso

lcs_sim = LCS_length / max(len(text1), len(text2))


# Resultado Final

## Fórmula de Combinación

Score_Final = w₁·S_semántica + w₂·S_léxica + w₃·S_estructural + w₄·S_secuencia

donde:
  w₁ + w₂ + w₃ + w₄ = 1.0

Pesos por defecto:
  w₁ = 0.40 (semántica)
  w₂ = 0.30 (léxica)
  w₃ = 0.20 (estructural)
  w₄ = 0.10 (secuencia)


## Umbrales de Clasificación


if score >= 0.75:
    return "PLAGIO MUY PROBABLE"
elif score >= 0.50:
    return "PLAGIO PROBABLE"
elif score >= 0.30:
    return "SIMILITUD SOSPECHOSA"
else:
    return "SIMILITUD BAJA"


# Preprocesamiento de Texto

## Pipeline de Limpieza


Texto Crudo
    ↓
Normalización Unicode (NFKC)
    ↓
Eliminación de URLs, emails
    ↓
Normalización de espacios
    ↓
Tokenización (NLTK)
    ↓
Lowercasing
    ↓
(Opcional) Eliminación de stopwords
    ↓
Texto Procesado


## Niveles de Limpieza

1. Light: Solo normalización básica
2. Medium (default): + eliminar URLs, emails
3. Aggressive: + eliminar números y acentos

# Entrenamiento y Optimización

## Optimización de Pesos

Método: Grid Search con validación cruzada


weight_ranges = {
    'semantic': [0.3, 0.4, 0.5],
    'lexical': [0.2, 0.3, 0.4],
    'structural': [0.1, 0.2, 0.3],
    'sequence': [0.05, 0.1, 0.15]
}

for combination in product(*weight_ranges.values()):
    normalize_weights(combination)
    f1_score = evaluate_on_validation_set()
    if f1_score > best_f1:
        best_weights = combination


## Optimización de Umbrales

Método: Búsqueda lineal sobre métrica objetivo

for threshold in np.arange(0.1, 1.0, 0.05):
    predictions = (scores >= threshold).astype(int)
    f1 = f1_score(true_labels, predictions)
    if f1 > best_f1:
        best_threshold = threshold


## Métricas de Evaluación

Accuracy = (TP + TN) / (TP + TN + FP + FN)
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1-Score = 2 × (Precision × Recall) / (Precision + Recall)

donde:
  TP = True Positives (plagio detectado correctamente)
  TN = True Negatives (no plagio detectado correctamente)
  FP = False Positives (falsa alarma)
  FN = False Negatives (plagio no detectado)


# Aplicaciones y Limitaciones

## Funciona para:

- Detección de parafraseo en textos académicos
- Comparación de artículos de noticias
- Análisis de ensayos y trabajos escritos
- Textos de 100-5000 palabras
- Idiomas: español, inglés, y otros 48+ idiomas

## Sus desventajas son:

- No detecta plagio por traducción automática
- Es menos preciso en textos muy cortos (<50 palabras)
- Podría fallar con lenguaje muy técnico
- Necesita una buena calidad de texto 

# Modelos Alternativos de Embeddings

Opción 1: Más rápido (menos preciso)

model_name = 'paraphrase-MiniLM-L6-v2'
Dimensión: 384, Velocidad: 2x más rápido


Opción 2: Más preciso (más lento)

model_name = 'paraphrase-multilingual-mpnet-base-v2'
Dimensión: 768, Precisión: +5-10% F1-score


Opción 3: Especializado en español

model_name = 'distiluse-base-multilingual-cased-v2'
Bueno para español


# Referencias

- Sentence-BERT: Reimers & Gurevych (2019) - Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
- TF-IDF: Salton & Buckley (1988)
- Jaccard Similarity: Jaccard (1901)
- NLTK: Bird, Klein & Loper (2009)
- spaCy: Honnibal & Montani (2017)

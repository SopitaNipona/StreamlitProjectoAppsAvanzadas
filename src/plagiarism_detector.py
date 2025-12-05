"""
plagiarism_detector.py
Detector de plagio usando análisis multidimensional

Autores: Alma Paulina González Sandoval, Diego Sánchez Valle
Fecha: Diciembre 2025

Este módulo implementa el detector principal que combina:
- Análisis semántico con embeddings de Sentence-BERT
- Análisis léxico (TF-IDF, Jaccard, n-gramas)
- Análisis estructural del texto
- Análisis de secuencias (LCS, SequenceMatcher)
"""

import numpy as np
import os
from typing import Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
import warnings

from text_preprocessor import TextPreprocessor
from similarity_metrics import SimilarityMetrics

warnings.filterwarnings('ignore')


class PlagiarismDetector:
    """
    Detector que combina múltiples técnicas de análisis
    """

    def __init__(self,
                 language: str = 'español',
                 model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2',
                 custom_weights: Optional[Dict[str, float]] = None):

        self.language = language
        self.preprocessor = TextPreprocessor(language=language)
        self.metrics_calculator = SimilarityMetrics()

        # Cargar modelo de embeddings semánticos
        print(f"Cargando modelo de embeddings: {model_name}...")
        self.embedding_model = SentenceTransformer(model_name)
        print("Modelo cargado exitosamente.")

        # Pesos por defecto para cada tipo de métrica
        self.weights = custom_weights or {
            'semantic': 0.40,      # Similitud semántica (embeddings)
            'lexical': 0.30,       # Similitud léxica (palabras, n-gramas)
            'structural': 0.20,    # Similitud estructural
            'sequence': 0.10,      # Similitud de secuencia
        }

        # Umbrales de detección
        self.thresholds = {
            'high_plagiarism': 0.75,      # >75% = plagio muy probable
            'moderate_plagiarism': 0.50,  # 50-75% = plagio probable
            'low_plagiarism': 0.30,       # 30-50% = similitud sospechosa
            # <30% = similitud baja/normal
        }

    def compute_semantic_similarity(self, text1: str, text2: str) -> float:
        # Generar embeddings
        embedding1 = self.embedding_model.encode(
            text1, convert_to_tensor=False)
        embedding2 = self.embedding_model.encode(
            text2, convert_to_tensor=False)

        # Calcular similitud coseno
        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

        return float(similarity)

    def compute_sentence_level_similarity(self, sentences1: list, sentences2: list) -> Dict[str, float]:
        """
        Calcula similitud a nivel de oraciones.
        """
        if not sentences1 or not sentences2:
            return {'avg_similarity': 0.0, 'max_similarity': 0.0, 'matched_sentences': 0}

        # Generar embeddings para todas las oraciones
        embeddings1 = self.embedding_model.encode(
            sentences1, convert_to_tensor=False)
        embeddings2 = self.embedding_model.encode(
            sentences2, convert_to_tensor=False)

        # Calcular matriz de similitud
        similarities = []
        matched_count = 0

        for emb1 in embeddings1:
            max_sim = 0.0
            for emb2 in embeddings2:
                sim = np.dot(emb1, emb2) / \
                    (np.linalg.norm(emb1) * np.linalg.norm(emb2))
                max_sim = max(max_sim, sim)

            similarities.append(max_sim)
            if max_sim > 0.7:  # Umbral para considerar oraciones coincidentes
                matched_count += 1

        return {
            'avg_similarity': float(np.mean(similarities)),
            'max_similarity': float(np.max(similarities)),
            'matched_sentences': matched_count,
            'match_ratio': matched_count / len(sentences1) if sentences1 else 0
        }

    def analyze_texts(self, text1: str, text2: str) -> Dict:
        """
        Análisis completo de similitud entre dos textos.
        """
        # Preprocesar textos
        clean_text1 = self.preprocessor.normalize_text(text1)
        clean_text2 = self.preprocessor.normalize_text(text2)

        # Tokenizar
        tokens1 = self.preprocessor.tokenize_words(clean_text1)
        tokens2 = self.preprocessor.tokenize_words(clean_text2)

        # Extraer características
        features1 = self.preprocessor.extract_features(text1)
        features2 = self.preprocessor.extract_features(text2)

        # Obtener oraciones
        sentences1 = self.preprocessor.tokenize_sentences(text1)
        sentences2 = self.preprocessor.tokenize_sentences(text2)

        # ANÁLISIS SEMÁNTICO - Usa embeddings de Sentence-BERT
        print("Calculando similitud semántica")
        semantic_overall = self.compute_semantic_similarity(
            clean_text1, clean_text2)
        sentence_level = self.compute_sentence_level_similarity(
            sentences1, sentences2)

        # Combinamos similitud global y a nivel de oraciones
        semantic_score = 0.6 * semantic_overall + \
            0.4 * sentence_level['avg_similarity']

        # ANÁLISIS LÉXICO - TF-IDF, Jaccard, n-gramas
        print("Calculando métricas léxicas")
        lexical_metrics = self.metrics_calculator.compute_all_metrics(
            clean_text1, clean_text2, tokens1, tokens2, features1, features2
        )

        # Combinar métricas léxicas
        lexical_score = np.mean([
            lexical_metrics['tfidf_cosine'],
            lexical_metrics['jaccard_words'],
            lexical_metrics['trigram_similarity'],
            lexical_metrics['dice_coefficient'],
        ])

        # ANÁLISIS ESTRUCTURAL
        structural_score = lexical_metrics['structural_similarity']

        # ANÁLISIS DE SECUENCIA
        sequence_score = np.mean([
            lexical_metrics['sequence_matcher'],
            lexical_metrics['lcs_ratio'],
        ])

        # RESULTADO FINAL PONDERADO
        final_score = (
            self.weights['semantic'] * semantic_score +
            self.weights['lexical'] * lexical_score +
            self.weights['structural'] * structural_score +
            self.weights['sequence'] * sequence_score
        )

        return {
            'final_score': final_score,
            'similarity_percentage': final_score * 100,

            'semantic': {
                'overall': semantic_overall,
                'sentence_avg': sentence_level['avg_similarity'],
                'matched_sentences': sentence_level['matched_sentences'],
                'match_ratio': sentence_level['match_ratio'],
                'score': semantic_score
            },

            'lexical': {
                'tfidf_cosine': lexical_metrics['tfidf_cosine'],
                'jaccard': lexical_metrics['jaccard_words'],
                'trigram': lexical_metrics['trigram_similarity'],
                'dice': lexical_metrics['dice_coefficient'],
                'score': lexical_score
            },

            'structural': {
                'similarity': structural_score,
                'score': structural_score
            },

            'sequence': {
                'sequence_matcher': lexical_metrics['sequence_matcher'],
                'lcs_ratio': lexical_metrics['lcs_ratio'],
                'score': sequence_score
            },

            'detailed_metrics': lexical_metrics,
            'features': {
                'text1': features1,
                'text2': features2
            }
        }

    def get_verdict(self, similarity_percentage: float) -> str:
        """
        Determina el veredicto basado en el porcentaje de similitud
        """
        if similarity_percentage >= self.thresholds['high_plagiarism'] * 100:
            return "Plagio muy probable - Alta similitud"
        elif similarity_percentage >= self.thresholds['moderate_plagiarism'] * 100:
            return "Plagio probable - Similitud moderada"
        elif similarity_percentage >= self.thresholds['low_plagiarism'] * 100:
            return "Plagio improbable - se recomienda hacer una revisión"
        else:
            return "Similitud baja - Texto original"

    def compare_texts(self, text1: str, text2: str) -> Dict:
        """
        Compara dos textos y retorna el análisis completo.
        """
        if not text1 or not text2:
            return {
                'error': 'Ambos textos deben tener contenido',
                'similarity_percentage': 0.0
            }

        analysis = self.analyze_texts(text1, text2)

        return {
            'similarity_percentage': analysis['similarity_percentage'],
            'final_score': analysis['final_score'],
            'verdict': self.get_verdict(analysis['similarity_percentage']),
            'breakdown': {
                'semantic': f"{analysis['semantic']['score'] * 100:.2f}%",
                'lexical': f"{analysis['lexical']['score'] * 100:.2f}%",
                'structural': f"{analysis['structural']['score'] * 100:.2f}%",
                'sequence': f"{analysis['sequence']['score'] * 100:.2f}%",
            },
            'details': analysis,
            'weights_used': self.weights
        }

    def compare_files(self, file1_path: str, file2_path: str, encoding: str = 'utf-8') -> Dict:
        """
        Compara dos archivos de texto.
        """
        try:
            with open(file1_path, 'r', encoding=encoding) as f:
                text1 = f.read()
        except Exception as e:
            return {'error': f'Error al leer archivo 1: {str(e)}'}

        try:
            with open(file2_path, 'r', encoding=encoding) as f:
                text2 = f.read()
        except Exception as e:
            return {'error': f'Error al leer archivo 2: {str(e)}'}

        result = self.compare_texts(text1, text2)
        result['files'] = {
            'file1': os.path.basename(file1_path),
            'file2': os.path.basename(file2_path)
        }

        return result

    def print_report(self, result: Dict):
        """
        Imprime un reporte formateado del análisis
        """
        if 'error' in result:
            print(f"\n Error: {result['error']}\n")
            return

        print("\n" + "="*70)
        print("Reporte de análisis de similitud")
        print("="*70)

        if 'files' in result:
            print(f"\n Archivo A: {result['files']['file1']}")
            print(f" Archivo B: {result['files']['file2']}")

        print(f"\n Similitud: {result['similarity_percentage']:.2f}%")
        print(f" Resultado: {result['verdict']}")

        print("\n" + "-"*70)
        print("Desglose por categorías:")
        print("-"*70)
        for category, percentage in result['breakdown'].items():
            print(f"  • {category.capitalize():15s}: {percentage}")

        print("\n" + "-"*70)
        print("Pesos utilizados:")
        print("-"*70)
        for key, value in result['weights_used'].items():
            print(f"  • {key.capitalize():15s}: {value:.2%}")

        print("\n" + "="*70 + "\n")

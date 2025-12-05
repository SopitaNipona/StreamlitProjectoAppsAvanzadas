"""
similarity_metrics.py
Cálculo de métricas de similitud entre textos

Autores: Alma Paulina González Sandoval, Diego Sánchez Valle
Fecha: Diciembre 2025

Implementa las métricas léxicas, estructurales y de secuencia:
- TF-IDF con similitud coseno
- Jaccard, Dice, Overlap
- N-gramas (bigrams, trigrams, 4-grams)
- LCS (Longest Common Subsequence)
- SequenceMatcher de Python
"""

import numpy as np
from typing import List, Dict, Tuple
from difflib import SequenceMatcher
from collections import Counter
import Levenshtein
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class SimilarityMetrics:
    "Calcula múltiples métricas de similitud entre dos textos"

    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer()

    def cosine_similarity_tfidf(self, text1: str, text2: str) -> float:
        """
        Calcula similitud coseno usando TF-IDF.

        Args:
            text1: Primer texto
            text2: Segundo texto

        Returns:
            Score de similitud [0, 1]
        """
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(
                tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0

    def jaccard_similarity(self, set1: set, set2: set) -> float:
        """
        Calcula similitud de Jaccard entre dos conjuntos.

        Args:
            set1: Primer conjunto
            set2: Segundo conjunto

        Returns:
            Score de similitud [0, 1]
        """
        if not set1 or not set2:
            return 0.0

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0.0

    def ngram_similarity(self, tokens1: List[str], tokens2: List[str], n: int = 3) -> float:
        """
        Calcula similitud basada en n-gramas comunes.

        Args:
            tokens1: Tokens del primer texto
            tokens2: Tokens del segundo texto
            n: Tamaño del n-grama

        Returns:
            Score de similitud [0, 1]
        """
        if len(tokens1) < n or len(tokens2) < n:
            return 0.0

        # Generar n-gramas
        ngrams1 = set(tuple(tokens1[i:i+n])
                      for i in range(len(tokens1) - n + 1))
        ngrams2 = set(tuple(tokens2[i:i+n])
                      for i in range(len(tokens2) - n + 1))

        return self.jaccard_similarity(ngrams1, ngrams2)

    def sequence_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud de secuencia usando SequenceMatcher.

        Args:
            text1: Primer texto
            text2: Segundo texto

        Returns:
            Score de similitud [0, 1]
        """
        return SequenceMatcher(None, text1, text2).ratio()

    def levenshtein_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud basada en distancia de Levenshtein normalizada.

        Args:
            text1: Primer texto
            text2: Segundo texto

        Returns:
            Score de similitud [0, 1]
        """
        max_len = max(len(text1), len(text2))
        if max_len == 0:
            return 1.0

        distance = Levenshtein.distance(text1, text2)
        return 1 - (distance / max_len)

    def containment_score(self, tokens1: List[str], tokens2: List[str]) -> Tuple[float, float]:
        """
        Calcula qué porcentaje de cada texto está contenido en el otro.

        Args:
            tokens1: Tokens del primer texto
            tokens2: Tokens del segundo texto

        Returns:
            Tupla (porcentaje de text1 en text2, porcentaje de text2 en text1)
        """
        if not tokens1 or not tokens2:
            return 0.0, 0.0

        set1 = set(tokens1)
        set2 = set(tokens2)

        containment_1_in_2 = len(set1.intersection(set2)) / len(set1)
        containment_2_in_1 = len(set2.intersection(set1)) / len(set2)

        return containment_1_in_2, containment_2_in_1

    def vocabulary_overlap(self, vocab1: set, vocab2: set) -> Dict[str, float]:
        """
        Analiza el solapamiento de vocabulario entre dos textos.

        Args:
            vocab1: Vocabulario del primer texto
            vocab2: Vocabulario del segundo texto

        Returns:
            Diccionario con métricas de solapamiento
        """
        if not vocab1 or not vocab2:
            return {
                'jaccard': 0.0,
                'overlap_coefficient': 0.0,
                'dice_coefficient': 0.0
            }

        intersection = len(vocab1.intersection(vocab2))
        union = len(vocab1.union(vocab2))
        min_size = min(len(vocab1), len(vocab2))

        return {
            'jaccard': intersection / union if union > 0 else 0.0,
            'overlap_coefficient': intersection / min_size if min_size > 0 else 0.0,
            'dice_coefficient': (2 * intersection) / (len(vocab1) + len(vocab2))
        }

    def structural_similarity(self, features1: Dict, features2: Dict) -> float:
        """
        Calcula similitud estructural basada en características del texto.

        Args:
            features1: Características del primer texto
            features2: Características del segundo texto

        Returns:
            Score de similitud [0, 1]
        """
        # Normalizar características numéricas
        metrics = []

        # Similitud en número de palabras
        word_diff = abs(features1['word_count'] - features2['word_count'])
        max_words = max(features1['word_count'], features2['word_count'])
        word_sim = 1 - (word_diff / max_words) if max_words > 0 else 0
        metrics.append(word_sim)

        # Similitud en número de oraciones
        sent_diff = abs(features1['sentence_count'] -
                        features2['sentence_count'])
        max_sents = max(features1['sentence_count'],
                        features2['sentence_count'])
        sent_sim = 1 - (sent_diff / max_sents) if max_sents > 0 else 0
        metrics.append(sent_sim)

        # Similitud en longitud promedio de palabras
        word_len_diff = abs(
            features1['avg_word_length'] - features2['avg_word_length'])
        max_word_len = max(
            features1['avg_word_length'], features2['avg_word_length'])
        word_len_sim = 1 - \
            (word_len_diff / max_word_len) if max_word_len > 0 else 0
        metrics.append(word_len_sim)

        # Similitud en longitud promedio de oraciones
        sent_len_diff = abs(
            features1['avg_sentence_length'] - features2['avg_sentence_length'])
        max_sent_len = max(
            features1['avg_sentence_length'], features2['avg_sentence_length'])
        sent_len_sim = 1 - \
            (sent_len_diff / max_sent_len) if max_sent_len > 0 else 0
        metrics.append(sent_len_sim)

        # Similitud en diversidad léxica
        lex_diff = abs(features1['lexical_diversity'] -
                       features2['lexical_diversity'])
        lex_sim = 1 - lex_diff
        metrics.append(lex_sim)

        return np.mean(metrics)

    def longest_common_subsequence(self, text1: str, text2: str) -> float:
        """
        Calcula el ratio del substring común más largo.

        Args:
            text1: Primer texto
            text2: Segundo texto

        Returns:
            Score de similitud [0, 1]
        """
        m = len(text1)
        n = len(text2)

        if m == 0 or n == 0:
            return 0.0

        # Matriz DP
        L = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif text1[i - 1] == text2[j - 1]:
                    L[i][j] = L[i - 1][j - 1] + 1
                else:
                    L[i][j] = max(L[i - 1][j], L[i][j - 1])

        lcs_length = L[m][n]
        max_length = max(m, n)

        return lcs_length / max_length if max_length > 0 else 0.0

    def compute_all_metrics(self, text1: str, text2: str, tokens1: List[str],
                            tokens2: List[str], features1: Dict, features2: Dict) -> Dict[str, float]:
        """
        Calcula todas las métricas de similitud.

        Args:
            text1: Primer texto normalizado
            text2: Segundo texto normalizado
            tokens1: Tokens del primer texto
            tokens2: Tokens del segundo texto
            features1: Características del primer texto
            features2: Características del segundo texto

        Returns:
            Diccionario con todas las métricas
        """
        vocab1 = features1['vocabulary']
        vocab2 = features2['vocabulary']
        vocab_metrics = self.vocabulary_overlap(vocab1, vocab2)
        containment = self.containment_score(tokens1, tokens2)

        metrics = {
            # Métricas léxicas
            'tfidf_cosine': self.cosine_similarity_tfidf(text1, text2),
            'jaccard_words': self.jaccard_similarity(set(tokens1), set(tokens2)),
            'jaccard_vocab': vocab_metrics['jaccard'],
            'dice_coefficient': vocab_metrics['dice_coefficient'],

            # Métricas de n-gramas
            'bigram_similarity': self.ngram_similarity(tokens1, tokens2, n=2),
            'trigram_similarity': self.ngram_similarity(tokens1, tokens2, n=3),
            'fourgram_similarity': self.ngram_similarity(tokens1, tokens2, n=4),

            # Métricas de secuencia
            'sequence_matcher': self.sequence_similarity(text1, text2),
            'levenshtein': self.levenshtein_similarity(text1, text2),
            'lcs_ratio': self.longest_common_subsequence(text1, text2),

            # Métricas estructurales
            'structural_similarity': self.structural_similarity(features1, features2),

            # Métricas de contención
            'containment_1_in_2': containment[0],
            'containment_2_in_1': containment[1],
            'max_containment': max(containment),
        }

        return metrics

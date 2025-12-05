"""
text_preprocessor.py
Preprocesamiento y limpieza de textos

Autores: Alma Paulina González Sandoval, Diego Sánchez Valle
Fecha: Diciembre 2025

Maneja la limpieza y normalización de textos antes del análisis.
Incluye tokenización, eliminación de stopwords y extracción de features.
"""

import re
import unicodedata
from typing import List, Set
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from unidecode import unidecode

# Descargar recursos de NLTK si no están disponibles
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class TextPreprocessor:
    "Preprocesador de texto con niveles de limpieza"

    def __init__(self, language: str = 'spanish', remove_stopwords: bool = False):
        """
            language: es el idioma del texto ('spanish', 'english')
            remove_stopwords: Si se deben eliminar stopwords
        """
        self.language = language
        self.remove_stopwords = remove_stopwords

        # Mapeo de idiomas
        lang_map = {
            'spanish': 'spanish',
            'es': 'spanish',
            'english': 'english',
            'en': 'english'
        }

        try:
            self.stopwords = set(stopwords.words(
                lang_map.get(language, 'spanish')))
        except:
            self.stopwords = set()

    def clean_text(self, text: str, level: str = 'medium') -> str:
        """
        Limpia el texto según el nivel especificado.
            text: Texto a limpiar
            level: Nivel de limpieza ('light', 'medium', 'aggressive')
        """
        if not text:
            return ""

        # Normalizar unicode
        text = unicodedata.normalize('NFKC', text)

        if level in ['medium', 'aggressive']:
            # Eliminar URLs
            text = re.sub(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

            # Eliminar emails
            text = re.sub(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

            # Eliminar números de teléfono
            text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text)

        if level == 'aggressive':
            # Eliminar todos los números
            text = re.sub(r'\d+', '', text)

            # Eliminar acentos
            text = unidecode(text)

        # Normalizar espacios en blanco
        text = re.sub(r'\s+', ' ', text)

        # Eliminar espacios al inicio y final
        text = text.strip()

        return text

    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokeniza el texto en palabras.

        Args:
            text: Texto a tokenizar

        Returns:
            Lista de tokens
        """
        try:
            tokens = word_tokenize(text.lower())
        except:
            # Fallback simple si NLTK falla
            tokens = re.findall(r'\b\w+\b', text.lower())

        # Filtrar tokens muy cortos
        tokens = [t for t in tokens if len(t) > 1]

        if self.remove_stopwords:
            tokens = [t for t in tokens if t not in self.stopwords]

        return tokens

    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Tokeniza el texto en oraciones.

        Args:
            text: Texto a tokenizar

        Returns:
            Lista de oraciones
        """
        try:
            sentences = sent_tokenize(text)
        except:
            # Fallback simple
            sentences = re.split(r'[.!?]+', text)

        return [s.strip() for s in sentences if s.strip()]

    def get_ngrams(self, tokens: List[str], n: int = 3) -> List[tuple]:
        """
        Genera n-gramas a partir de tokens.

        Args:
            tokens: Lista de tokens
            n: Tamaño del n-grama

        Returns:
            Lista de n-gramas
        """
        if len(tokens) < n:
            return []

        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

    def extract_features(self, text: str) -> dict:
        """
        Extrae características del texto para análisis.

        Args:
            text: Texto a analizar

        Returns:
            Diccionario con características
        """
        sentences = self.tokenize_sentences(text)
        tokens = self.tokenize_words(text)

        return {
            'char_count': len(text),
            'word_count': len(tokens),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(w) for w in tokens) / len(tokens) if tokens else 0,
            'avg_sentence_length': len(tokens) / len(sentences) if sentences else 0,
            'unique_words': len(set(tokens)),
            'lexical_diversity': len(set(tokens)) / len(tokens) if tokens else 0,
            'vocabulary': set(tokens)
        }

    def normalize_text(self, text: str) -> str:
        """
        Normaliza texto para comparación semántica.

        Args:
            text: Texto a normalizar

        Returns:
            Texto normalizado
        """
        # Limpiar
        text = self.clean_text(text, level='medium')

        # Convertir a minúsculas
        text = text.lower()

        # Normalizar puntuación
        text = re.sub(r'[^\w\s]', ' ', text)

        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text).strip()

        return text

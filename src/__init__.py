"""
Modelo de Detección de Plagio y Similitud de Textos
"""

from .plagiarism_detector import PlagiarismDetector
from .text_preprocessor import TextPreprocessor
from .similarity_metrics import SimilarityMetrics
from .model_trainer import PlagiarismModelTrainer

__version__ = '1.0.0'

__all__ = [
    'PlagiarismDetector',
    'TextPreprocessor',
    'SimilarityMetrics',
    'PlagiarismModelTrainer',
]

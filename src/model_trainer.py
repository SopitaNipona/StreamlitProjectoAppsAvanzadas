"""
model_trainer.py
Entrenamiento y optimización del detector de plagio

Autores: Alma Paulina González Sandoval, Diego Sánchez Valle
Fecha: Diciembre 2025

Este módulo optimiza los pesos y umbrales del detector usando grid search.
Evalúa el rendimiento con métricas estándar (Accuracy, Precision, Recall, F1).
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import json
import os
from tqdm import tqdm

from plagiarism_detector import PlagiarismDetector


class PlagiarismModelTrainer:

    def __init__(self, detector: Optional[PlagiarismDetector] = None):
        self.detector = detector or PlagiarismDetector()
        self.training_results = []

    def load_dataset(self, dataset_path: str) -> pd.DataFrame:

        try:
            df = pd.read_csv(dataset_path)
            required_columns = ['text1', 'text2', 'is_plagiarism']

            if not all(col in df.columns for col in required_columns):
                raise ValueError(
                    f"El dataset debe contener las columnas: {required_columns}")

            print(f" Dataset cargado: {len(df)} pares de textos")
            print(f" Plagio: {df['is_plagiarism'].sum()}")
            print(f" No plagio/original {(~df['is_plagiarism']).sum()}")

            return df

        except Exception as e:
            raise Exception(f"Error al cargar el dataset: {str(e)}")

    def evaluate_on_dataset(self, df: pd.DataFrame, threshold: float = 0.5) -> Dict:

        predictions = []
        true_labels = []
        scores = []

        print("Evaluando en el dataset")
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            result = self.detector.compare_texts(row['text1'], row['text2'])

            if 'error' in result:
                continue

            score = result['final_score']
            prediction = 1 if score >= threshold else 0

            predictions.append(prediction)
            true_labels.append(int(row['is_plagiarism']))
            scores.append(score)

        # Calculo de métricas
        accuracy = accuracy_score(true_labels, predictions)
        precision = precision_score(true_labels, predictions, zero_division=0)
        recall = recall_score(true_labels, predictions, zero_division=0)
        f1 = f1_score(true_labels, predictions, zero_division=0)
        conf_matrix = confusion_matrix(true_labels, predictions)

        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': conf_matrix,
            'scores': scores,
            'predictions': predictions,
            'true_labels': true_labels,
            'threshold_used': threshold
        }

    def optimize_threshold(self, df: pd.DataFrame, metric: str = 'f1_score') -> Tuple[float, Dict]:
        thresholds = np.arange(0.1, 1.0, 0.05)
        best_threshold = 0.5
        best_score = 0.0
        best_metrics = {}

        print(f"Optimizando umbral basado en {metric}")

        for threshold in tqdm(thresholds):
            metrics = self.evaluate_on_dataset(df, threshold=threshold)
            current_score = metrics[metric]

            if current_score > best_score:
                best_score = current_score
                best_threshold = threshold
                best_metrics = metrics

        print(f"\n Mejor umbral encontrado: {best_threshold:.2f}")
        print(f"  {metric}: {best_score:.4f}")

        return best_threshold, best_metrics

    def grid_search_weights(self, df: pd.DataFrame,
                            weight_ranges: Optional[Dict[str, List[float]]] = None) -> Dict:

        if weight_ranges is None:
            weight_ranges = {
                'semantic': [0.3, 0.4, 0.5],
                'lexical': [0.2, 0.3, 0.4],
                'structural': [0.1, 0.2, 0.3],
                'sequence': [0.05, 0.1, 0.15]
            }

        best_f1 = 0.0
        best_weights = None

        print("Realizando búsqueda de mejores pesos")

        from itertools import product

        combinations = list(product(
            weight_ranges['semantic'],
            weight_ranges['lexical'],
            weight_ranges['structural'],
            weight_ranges['sequence']
        ))

        for sem, lex, struc, seq in tqdm(combinations):
            # Normalizar para que sumen 1
            total = sem + lex + struc + seq
            weights = {
                'semantic': sem / total,
                'lexical': lex / total,
                'structural': struc / total,
                'sequence': seq / total
            }

            # Actualizar pesos del detector
            self.detector.weights = weights

            # Evaluar
            metrics = self.evaluate_on_dataset(df, threshold=0.5)
            f1 = metrics['f1_score']

            if f1 > best_f1:
                best_f1 = f1
                best_weights = weights.copy()

        print(f"\n Mejores pesos encontrados (F1: {best_f1:.4f}):")
        for key, value in best_weights.items():
            print(f"  {key}: {value:.3f}")

        return best_weights

    def train(self, dataset_path: str, optimize_weights: bool = True,
              optimize_threshold: bool = True, test_size: float = 0.2) -> Dict:

        # Cargar datos
        df = self.load_dataset(dataset_path)

        # Split train/test
        train_df, test_df = train_test_split(df, test_size=test_size, random_state=42,
                                             stratify=df['is_plagiarism'])

        print(f"\n Train: {len(train_df)} Test: {len(test_df)}")

        results = {
            'train_size': len(train_df),
            'test_size': len(test_df)
        }

        if optimize_weights:
            print("\n" + "="*70)
            print("Fase 1: optimización de pesos")
            print("="*70)
            best_weights = self.grid_search_weights(train_df)
            self.detector.weights = best_weights
            results['optimized_weights'] = best_weights
        else:
            results['optimized_weights'] = self.detector.weights

        if optimize_threshold:
            print("\n" + "="*70)
            print("Fase 2: optimización de umbral")
            print("="*70)
            best_threshold, _ = self.optimize_threshold(
                train_df, metric='f1_score')
            self.detector.thresholds['moderate_plagiarism'] = best_threshold
            results['optimized_threshold'] = best_threshold
        else:
            results['optimized_threshold'] = self.detector.thresholds['moderate_plagiarism']

        # Evaluación final
        print("\n" + "="*70)
        print("Evaluación final")
        print("="*70)
        test_metrics = self.evaluate_on_dataset(
            test_df,
            threshold=results['optimized_threshold']
        )

        results['test_metrics'] = {
            'accuracy': test_metrics['accuracy'],
            'precision': test_metrics['precision'],
            'recall': test_metrics['recall'],
            'f1_score': test_metrics['f1_score'],
            'confusion_matrix': test_metrics['confusion_matrix'].tolist()
        }

        self.print_training_results(results)

        return results

    def save_model_config(self, output_path: str, results: Dict):

        config = {
            'weights': results['optimized_weights'],
            'threshold': results['optimized_threshold'],
            'test_metrics': results['test_metrics'],
            'language': self.detector.language
        }

        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"\n Configuración guardada en {output_path}")

    def load_model_config(self, config_path: str):
        with open(config_path, 'r') as f:
            config = json.load(f)

        self.detector.weights = config['weights']
        self.detector.thresholds['moderate_plagiarism'] = config['threshold']

        print(f"Configuración cargada desde {config_path}")

    def print_training_results(self, results: Dict):

        print("\n" + "="*70)
        print("RESULTADOS DEL ENTRENAMIENTO")
        print("="*70)

        print("\n Métricas en test:")
        metrics = results['test_metrics']
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-Score:  {metrics['f1_score']:.4f}")

        print("\n Pesos optimizados:")
        for key, value in results['optimized_weights'].items():
            print(f"  {key.capitalize():12s}: {value:.3f}")

        print(f"\n Umbral optimizado: {results['optimized_threshold']:.3f}")

        print("\n" + "="*70 + "\n")

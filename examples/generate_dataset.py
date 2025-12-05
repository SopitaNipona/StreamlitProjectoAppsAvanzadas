"""
Script para generar un dataset de entrenamiento sintético.
Crea pares de textos con diferentes niveles de similitud.
"""

import pandas as pd
import numpy as np
import os
from typing import List, Tuple


class DatasetGenerator:
    """Generador de datasets sintéticos para entrenamiento."""

    def __init__(self):
        """Inicializa el generador."""
        self.original_texts = [
            """La inteligencia artificial es una rama de la informática que busca crear
            sistemas capaces de realizar tareas que normalmente requieren inteligencia
            humana, como el aprendizaje, el razonamiento y la resolución de problemas.""",

            """El aprendizaje automático permite a las computadoras aprender de los datos
            sin ser explícitamente programadas. Utiliza algoritmos estadísticos para
            identificar patrones y hacer predicciones basadas en ejemplos.""",

            """El procesamiento del lenguaje natural es una disciplina que combina
            lingüística e inteligencia artificial para permitir que las máquinas
            comprendan y generen lenguaje humano de manera efectiva.""",

            """Las redes neuronales artificiales están inspiradas en el funcionamiento
            del cerebro humano. Consisten en capas de nodos interconectados que procesan
            información de manera distribuida para resolver problemas complejos.""",

            """El deep learning ha revolucionado campos como la visión por computadora
            y el reconocimiento de voz. Utiliza redes neuronales profundas con múltiples
            capas para aprender representaciones jerárquicas de los datos.""",

            """La ética en inteligencia artificial es un tema crítico en la actualidad.
            Es fundamental desarrollar sistemas de IA que sean justos, transparentes
            y respeten la privacidad y los derechos de las personas.""",

            """Los algoritmos de clasificación son fundamentales en el aprendizaje
            supervisado. Aprenden a categorizar datos en clases predefinidas mediante
            el análisis de ejemplos etiquetados durante el entrenamiento.""",

            """El reconocimiento de imágenes utiliza técnicas de visión por computadora
            para identificar objetos, personas y escenas en fotografías. Los modelos
            modernos pueden alcanzar precisión superior a la humana en tareas específicas.""",

            """Los chatbots utilizan procesamiento del lenguaje natural para mantener
            conversaciones con usuarios. Pueden responder preguntas, proporcionar
            asistencia y realizar tareas automatizadas de manera conversacional.""",

            """El aprendizaje por refuerzo permite a los agentes aprender mediante
            interacción con su entorno. Reciben recompensas o penalizaciones según
            sus acciones, optimizando su comportamiento con el tiempo.""",
        ]

    def create_paraphrase(self, text: str, level: str = 'medium') -> str:
        """
        Crea una paráfrasis del texto.

        Args:
            text: Texto original
            level: Nivel de parafraseo ('light', 'medium', 'heavy')

        Returns:
            Texto parafraseado
        """
        # Mapeos de palabras comunes para parafraseo
        replacements_light = {
            'permite': 'facilita',
            'crear': 'desarrollar',
            'sistemas': 'programas',
            'utiliza': 'emplea',
            'aprender': 'adquirir conocimiento',
            'datos': 'información',
            'computadoras': 'ordenadores',
            'fundamentales': 'esenciales',
            'mediante': 'a través de',
            'múltiples': 'varias',
        }

        replacements_medium = {
            **replacements_light,
            'inteligencia artificial': 'IA',
            'aprendizaje automático': 'machine learning',
            'procesamiento del lenguaje natural': 'PLN',
            'redes neuronales': 'neural networks',
            'deep learning': 'aprendizaje profundo',
            'visión por computadora': 'computer vision',
            'algoritmos': 'métodos computacionales',
            'pueden': 'tienen la capacidad de',
            'permite a las': 'posibilita que las',
        }

        replacements_heavy = {
            **replacements_medium,
            'es una': 'constituye una',
            'que busca': 'cuyo objetivo es',
            'capaces de': 'con la habilidad de',
            'normalmente': 'típicamente',
            'como': 'tales como',
            'sin ser': 'sin necesidad de ser',
            'basadas en': 'fundamentadas en',
        }

        replacements = {
            'light': replacements_light,
            'medium': replacements_medium,
            'heavy': replacements_heavy
        }[level]

        paraphrased = text
        for old, new in replacements.items():
            paraphrased = paraphrased.replace(old, new)

        return paraphrased

    def create_partial_copy(self, text: str, percentage: float = 0.5) -> str:
        """
        Crea una copia parcial del texto.

        Args:
            text: Texto original
            percentage: Porcentaje del texto a mantener

        Returns:
            Copia parcial del texto
        """
        sentences = text.split('.')
        num_to_keep = max(1, int(len(sentences) * percentage))
        kept_sentences = sentences[:num_to_keep]

        # Agregar texto diferente al final
        additional = " Los avances tecnológicos continúan transformando nuestra sociedad."

        return '.'.join(kept_sentences) + additional

    def create_different_text(self) -> str:
        """Genera un texto completamente diferente."""
        different_texts = [
            """El cambio climático es uno de los mayores desafíos de nuestro tiempo.
            Las emisiones de gases de efecto invernadero están causando un aumento
            en las temperaturas globales y eventos climáticos extremos.""",

            """La literatura del siglo XIX reflejaba las transformaciones sociales
            de la era industrial. Autores como Dickens y Balzac retrataron las
            condiciones de vida de las clases trabajadoras.""",

            """La gastronomía mediterránea se caracteriza por el uso de aceite de oliva,
            vegetales frescos y pescado. Es considerada una de las dietas más saludables
            del mundo por sus beneficios cardiovasculares.""",

            """El sistema solar está compuesto por ocho planetas que orbitan alrededor
            del Sol. Cada planeta tiene características únicas en cuanto a tamaño,
            composición y condiciones atmosféricas.""",

            """La música clásica europea del período barroco se caracteriza por
            su ornamentación elaborada y el uso del bajo continuo. Compositores
            como Bach y Händel definieron este estilo musical.""",
        ]

        return np.random.choice(different_texts)

    def generate_dataset(self, num_samples: int = 200) -> pd.DataFrame:
        """
        Genera un dataset balanceado de pares de textos.

        Args:
            num_samples: Número total de muestras a generar

        Returns:
            DataFrame con el dataset
        """
        data = []

        num_plagiarism = num_samples // 2
        num_non_plagiarism = num_samples - num_plagiarism

        print(f"Generando dataset con {num_samples} muestras...")

        # Casos de plagio
        for i in range(num_plagiarism):
            original = np.random.choice(self.original_texts)

            # Diferentes tipos de plagio
            plagiarism_type = np.random.choice([
                'identical',
                'light_paraphrase',
                'medium_paraphrase',
                'heavy_paraphrase',
                'partial_copy'
            ])

            if plagiarism_type == 'identical':
                modified = original
            elif plagiarism_type == 'light_paraphrase':
                modified = self.create_paraphrase(original, 'light')
            elif plagiarism_type == 'medium_paraphrase':
                modified = self.create_paraphrase(original, 'medium')
            elif plagiarism_type == 'heavy_paraphrase':
                modified = self.create_paraphrase(original, 'heavy')
            else:  # partial_copy
                modified = self.create_partial_copy(original)

            data.append({
                'text1': original.strip(),
                'text2': modified.strip(),
                'is_plagiarism': True,
                'plagiarism_type': plagiarism_type
            })

        # Casos de no plagio
        for i in range(num_non_plagiarism):
            text1 = np.random.choice(self.original_texts)
            text2 = self.create_different_text()

            data.append({
                'text1': text1.strip(),
                'text2': text2.strip(),
                'is_plagiarism': False,
                'plagiarism_type': 'none'
            })

        df = pd.DataFrame(data)

        # Shuffle
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)

        print(f"✓ Dataset generado:")
        print(f"  - Total: {len(df)} muestras")
        print(f"  - Plagio: {df['is_plagiarism'].sum()}")
        print(f"  - No plagio: {(~df['is_plagiarism']).sum()}")

        return df


def main():
    """Genera y guarda el dataset."""
    # Crear generador
    generator = DatasetGenerator()

    # Generar dataset
    df = generator.generate_dataset(num_samples=200)

    # Crear directorio si no existe
    output_dir = "../data/training"
    os.makedirs(output_dir, exist_ok=True)

    # Guardar
    output_path = os.path.join(output_dir, "plagiarism_dataset.csv")
    df.to_csv(output_path, index=False)

    print(f"\n✓ Dataset guardado en: {output_path}")
    print(f"\nPrimeras 5 filas:")
    print(df.head())


if __name__ == "__main__":
    main()

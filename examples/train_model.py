"""
train_model.py
Entrenamiento del detector con dataset de PAN-2011

Autores: Alma Paulina González Sandoval, Diego Sánchez Valle
Fecha: Diciembre 2025

Optimiza pesos y umbrales usando el dataset combinado.
Genera métricas de evaluación (Accuracy, Precision, Recall, F1).
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from plagiarism_detector import PlagiarismDetector
from model_trainer import PlagiarismModelTrainer


def train_with_dataset():
    """
    Entrena el modelo usando un dataset etiquetado
    """
    print("\n" + "="*70)
    print("Entrenamiento del modelo de detección de plagio")
    print("="*70)

    # Buscar dataset combinado primero
    dataset_options = [
        "../data/training/combined_dataset.csv",
        "../data/training/pan2011_dataset.csv",
        "../data/training/plagiarism_dataset.csv"
    ]

    dataset_path = None
    for path in dataset_options:
        if os.path.exists(path):
            dataset_path = path
            print(f"\n✓ Usando dataset: {os.path.basename(path)}")
            break

    if not dataset_path:
        print(f"\n No se encontró ningún dataset")
        print("\nPara entrenar el modelo, necesitas un dataset CSV con el formato:")
        print("  text1,text2,is_plagiarism")
        print("\nOpciones:")
        print("  1. python process_pan2011.py (datos reales de PAN)")
        print("  2. python generate_dataset.py (datos sintéticos)")
        print("  3. python combine_datasets.py (combinar ambos)")
        return

    # Crear detector
    detector = PlagiarismDetector(language='spanish')

    # Crear entrenador
    trainer = PlagiarismModelTrainer(detector)

    # Entrenar
    results = trainer.train(
        dataset_path=dataset_path,
        optimize_weights=True,
        optimize_threshold=True,
        test_size=0.2
    )

    # Guardar configuración optimizada
    output_path = "../models/optimized_config.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    trainer.save_model_config(output_path, results)

    print("\n✓ Entrenamiento completado")
    print(f"✓ Configuración guardada en: {output_path}")


def use_pretrained_model():
    """
    Usa un modelo previamente entrenado.
    """
    print("\n" + "="*70)
    print("USANDO MODELO PRE-ENTRENADO")
    print("="*70)

    config_path = "../models/optimized_config.json"

    if not os.path.exists(config_path):
        print(f"\n Configuración no encontrada: {config_path}")
        print("\nPrimero entrena el modelo usando train_with_dataset()")
        return

    # Crear detector
    detector = PlagiarismDetector(language='spanish')

    # Crear entrenador y cargar configuración
    trainer = PlagiarismModelTrainer(detector)
    trainer.load_model_config(config_path)

    # Probar con textos de ejemplo
    texto_a = """
    La inteligencia artificial está transformando la manera en que vivimos
    y trabajamos. Los sistemas de IA pueden procesar grandes cantidades de
    datos y extraer insights valiosos que ayudan en la toma de decisiones.
    """

    texto_b = """
    La IA está revolucionando nuestra forma de vida y trabajo. Estos sistemas
    tienen la capacidad de analizar enormes volúmenes de información y obtener
    conocimientos importantes que facilitan las decisiones estratégicas.
    """

    resultado = detector.compare_texts(texto_a, texto_b)
    detector.print_report(resultado)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "use":
        # Usar modelo pre-entrenado
        use_pretrained_model()
    else:
        # Entrenar el modelo (por defecto)
        train_with_dataset()

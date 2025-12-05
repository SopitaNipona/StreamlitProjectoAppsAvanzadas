"""
quick_comparison.py
Comparación rápida de dos archivos de texto

Autores: Alma Paulina González Sandoval, Diego Sánchez Valle
Fecha: Diciembre 2025

Uso: python quick_comparison.py archivo1.txt archivo2.txt
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from plagiarism_detector import PlagiarismDetector


def main():
    "Compara dos archivos"

    if len(sys.argv) != 3:
        print("\n Uso incorrecto")
        print(f"\nUso: python {sys.argv[0]} archivo1.txt archivo2.txt")
        print("\nEjemplo:")
        print(f"  python {sys.argv[0]} documento_A.txt documento_B.txt")
        sys.exit(1)

    archivo1 = sys.argv[1]
    archivo2 = sys.argv[2]

    # Verificar que los archivos existan
    if not os.path.exists(archivo1):
        print(f"\n Error: No se encuentra el archivo '{archivo1}'")
        sys.exit(1)

    if not os.path.exists(archivo2):
        print(f"\n Error: No se encuentra el archivo '{archivo2}'")
        sys.exit(1)

    # Detectar idioma (simple heurística basada en extensión o contenido)
    print("\n Inicializando detector de plagio...")

    # Por defecto usar español, pero puedes cambiar esto
    language = 'spanish'

    detector = PlagiarismDetector(language=language)

    # Comparar archivos
    print(f"\n Comparando archivos...")
    print(f"   A: {archivo1}")
    print(f"   B: {archivo2}")

    resultado = detector.compare_files(archivo1, archivo2)

    # Mostrar resultado
    detector.print_report(resultado)

    # Retornar código de salida basado en el nivel de similitud
    similarity = resultado.get('similarity_percentage', 0)

    if similarity >= 75:
        sys.exit(2)  # Plagio muy probable
    elif similarity >= 50:
        sys.exit(1)  # Plagio probable
    else:
        sys.exit(0)  # OK


if __name__ == "__main__":
    main()

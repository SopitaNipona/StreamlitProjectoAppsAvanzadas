"""
compare_texts.py
Ejemplos de uso del detector de plagio

Autores: Alma Paulina González Sandoval, Diego Sánchez Valle
Fecha: Diciembre 2025

Script de demostración con varios casos de prueba.
"""

from plagiarism_detector import PlagiarismDetector
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def example_1_texto_identico():
    print("\n" + "="*10)
    print("Ejemplo 1: textos iguales")
    print("="*70)

    texto = """
    La inteligencia artificial es una rama de la informática que busca crear
    sistemas capaces de realizar tareas que normalmente requieren inteligencia
    humana. Esto incluye el aprendizaje, el razonamiento y la auto-corrección.
    """

    detector = PlagiarismDetector(language='español')
    resultado = detector.compare_texts(texto, texto)
    detector.print_report(resultado)


def example_2_parafraseo():
    print("\n" + "="*70)
    print("Ejemplo 2: parafraseo")
    print("="*70)

    texto_a = """
    La inteligencia artificial es una rama de la informática que busca crear
    sistemas capaces de realizar tareas que normalmente requieren inteligencia
    humana. Esto incluye el aprendizaje, el razonamiento y la auto-corrección.
    Los sistemas de IA pueden analizar datos, reconocer patrones y tomar
    decisiones basadas en la información disponible.
    """

    texto_b = """
    La IA constituye un área de las ciencias computacionales enfocada en
    desarrollar programas que puedan ejecutar actividades que típicamente
    necesitan capacidad intelectual humana. Entre estas actividades se
    encuentran el proceso de aprendizaje, el pensamiento lógico y la
    capacidad de autocorrección. Los programas de inteligencia artificial
    tienen la habilidad de examinar información, identificar tendencias
    y realizar elecciones fundamentadas en los datos que tienen a su disposición.
    """

    detector = PlagiarismDetector(language='español')
    resultado = detector.compare_texts(texto_a, texto_b)
    detector.print_report(resultado)


def example_3_textos_diferentes():
    print("\n" + "="*70)
    print("Ejemplo 3: textos diferentes")
    print("="*70)

    texto_a = """
    La inteligencia artificial está revolucionando múltiples industrias,
    desde la medicina hasta las finanzas. Los algoritmos de aprendizaje
    automático pueden detectar patrones que son invisibles para el ojo humano.
    """

    texto_b = """
    El cambio climático representa uno de los mayores desafíos de nuestro
    tiempo. Las emisiones de gases de efecto invernadero están causando
    un aumento en las temperaturas globales, lo que resulta en eventos
    climáticos extremos más frecuentes.
    """

    detector = PlagiarismDetector(language='español')
    resultado = detector.compare_texts(texto_a, texto_b)
    detector.print_report(resultado)


def example_4_plagio_parcial():
    print("\n" + "="*70)
    print("Ejemplo 4: plagio parcial")
    print("="*70)

    texto_a = """
    El aprendizaje automático es un subcampo de la inteligencia artificial
    que permite a las computadoras aprender sin ser explícitamente programadas.
    Utiliza algoritmos que pueden mejorar automáticamente a través de la experiencia.
    Los modelos de aprendizaje profundo han demostrado ser particularmente efectivos
    en tareas como el reconocimiento de imágenes y el procesamiento del lenguaje natural.
    """

    texto_b = """
    En el contexto de la programación moderna, el aprendizaje automático
    representa una innovación importante. Utiliza algoritmos que pueden
    mejorar automáticamente a través de la experiencia, lo cual es fundamental
    para muchas aplicaciones actuales. Además, permite desarrollar sistemas
    más adaptativos y robustos que los métodos tradicionales de programación.
    """

    detector = PlagiarismDetector(language='español')
    resultado = detector.compare_texts(texto_a, texto_b)
    detector.print_report(resultado)


def example_5_archivos():
    print("\n" + "="*70)
    print("Ejemlpo 5: comparar archivos")
    print("="*70)

   # archivos de ejemplo
    archivo_a = "/tmp/texto_a.txt"
    archivo_b = "/tmp/texto_b.txt"

    texto_a = """
    El procesamiento del lenguaje natural (PLN) es una disciplina que
    combina la lingüística, la informática y la inteligencia artificial.
    Su objetivo es permitir que las computadoras entiendan, interpreten
    y generen lenguaje humano de manera significativa.
    """

    texto_b = """
    El PLN es un área que fusiona lingüística, ciencias de la computación
    e inteligencia artificial. Busca facilitar que los ordenadores comprendan,
    analicen y produzcan lenguaje humano de forma relevante y coherente.
    """

    with open(archivo_a, 'w', encoding='utf-8') as f:
        f.write(texto_a)

    with open(archivo_b, 'w', encoding='utf-8') as f:
        f.write(texto_b)

    # Comparar
    detector = PlagiarismDetector(language='spanish')
    resultado = detector.compare_files(archivo_a, archivo_b)
    detector.print_report(resultado)

    # Limpiar
    os.remove(archivo_a)
    os.remove(archivo_b)


def example_6_ingles():
    print("\n" + "="*70)
    print("Ejemplo 6: textos en ingles")
    print("="*70)

    text_a = """
    Machine learning is a subset of artificial intelligence that enables
    computers to learn without being explicitly programmed. It uses algorithms
    that can automatically improve through experience and data analysis.
    """

    text_b = """
    ML represents a branch of AI that allows computer systems to learn
    automatically without explicit programming. These algorithms enhance
    their performance by analyzing data and gaining experience over time.
    """

    detector = PlagiarismDetector(language='english')
    resultado = detector.compare_texts(text_a, text_b)
    detector.print_report(resultado)


def main():
    print("\n" + "="*70)
    print("demostración de PlagiarismDetector")
    print("="*70)

    # Ejecutar ejemplos
    example_1_texto_identico()
    example_2_parafraseo()
    example_3_textos_diferentes()
    example_4_plagio_parcial()
    example_5_archivos()
    example_6_ingles()

    print("\n Demstración completa \n")


if __name__ == "__main__":
    main()

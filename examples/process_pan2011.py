"""
process_pan2011.py
Procesador del PAN Plagiarism Corpus 2011

Autores: Alma Paulina González Sandoval, Diego Sánchez Valle
Fecha: Diciembre 2025

Extrae pares de textos del corpus PAN-2011 para entrenamiento.
Genera dataset balanceado con casos positivos y negativos.
"""

import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
from tqdm import tqdm
import random


class PAN2011Processor:
    "Procesador para PAN-2011"

    def __init__(self, corpus_path: str):
        self.corpus_path = Path(corpus_path)
        self.external_path = self.corpus_path / "external-detection-corpus"
        self.source_path = self.external_path / "source-document"
        self.suspicious_path = self.external_path / "suspicious-document"

        self.data = []

    def read_text_file(self, file_path: Path) -> str:
        """Lee un archivo de texto."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
                # Limitar a primeros 2000 caracteres para evitar textos muy largos
                return content[:2000] if len(content) > 2000 else content
        except Exception as e:
            print(f"⚠️  Error leyendo {file_path}: {e}")
            return ""

    def parse_xml_annotations(self, xml_file: Path) -> list:
        """
        Parsea el archivo XML de anotaciones de PAN.

        Returns:
            Lista de diccionarios con información de plagio
        """
        plagiarism_sections = []

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Buscar todas las características de plagio
            for feature in root.findall('.//feature'):
                source_ref = feature.get('source_reference', '')
                source_offset = int(feature.get('source_offset', 0))
                source_length = int(feature.get('source_length', 0))
                this_offset = int(feature.get('this_offset', 0))
                this_length = int(feature.get('this_length', 0))
                obfuscation = feature.get('obfuscation', 'none')

                if source_ref:
                    plagiarism_sections.append({
                        'source_file': source_ref,
                        'source_offset': source_offset,
                        'source_length': source_length,
                        'this_offset': this_offset,
                        'this_length': this_length,
                        'obfuscation': obfuscation
                    })

        except Exception as e:
            # Archivo sin plagio (muchos archivos sospechosos no tienen plagio)
            pass

        return plagiarism_sections

    def extract_text_section(self, text: str, offset: int, length: int) -> str:
        """Extrae una sección específica del texto."""
        if length <= 0 or offset < 0:
            return text[:500]  # Retornar primeros 500 chars si no hay info
        return text[offset:offset + length]

    def process_suspicious_document(self, susp_file: Path, xml_file: Path):
        """Procesa un documento sospechoso y sus anotaciones."""

        # Leer texto sospechoso
        susp_text = self.read_text_file(susp_file)
        if not susp_text or len(susp_text) < 50:
            return

        # Parsear anotaciones
        plagiarism_sections = self.parse_xml_annotations(xml_file)

        if plagiarism_sections:
            # HAY PLAGIO - procesar cada sección
            for section in plagiarism_sections:
                # Encontrar archivo fuente
                source_filename = section['source_file']

                # Buscar en todas las partes
                source_file = None
                for part_dir in self.source_path.iterdir():
                    if part_dir.is_dir():
                        potential_file = part_dir / source_filename
                        if potential_file.exists():
                            source_file = potential_file
                            break

                if source_file and source_file.exists():
                    source_text = self.read_text_file(source_file)

                    if source_text and len(source_text) > 50:
                        # Extraer secciones específicas si es posible
                        if section['source_length'] > 0:
                            source_section = self.extract_text_section(
                                source_text,
                                section['source_offset'],
                                section['source_length']
                            )
                        else:
                            source_section = source_text

                        if section['this_length'] > 0:
                            susp_section = self.extract_text_section(
                                susp_text,
                                section['this_offset'],
                                section['this_length']
                            )
                        else:
                            susp_section = susp_text

                        # Agregar par de plagio
                        if len(source_section) > 50 and len(susp_section) > 50:
                            self.data.append({
                                'text1': source_section,
                                'text2': susp_section,
                                'is_plagiarism': True,
                                'plagiarism_type': section['obfuscation']
                            })
        else:
            # NO HAY PLAGIO - este documento es original
            # Lo usaremos para generar pares negativos
            pass

    def process_all_documents(self, max_pairs: int = 1000):
        """
        Procesa todos los documentos del corpus.

        Args:
            max_pairs: Número máximo de pares a procesar
        """
        print("\n Procesando PAN-2011 External Detection Corpus...")
        print(f" Ruta: {self.external_path}")

        # Recolectar todos los archivos sospechosos
        suspicious_files = []

        for part_dir in self.suspicious_path.iterdir():
            if part_dir.is_dir() and part_dir.name.startswith('part'):
                xml_files = list(part_dir.glob("*.xml"))
                suspicious_files.extend(xml_files)

        print(f" Encontrados {len(suspicious_files)} documentos sospechosos")

        # Procesar archivos sospechosos (casos de plagio)
        print("\n Procesando casos de plagio...")

        processed = 0
        for xml_file in tqdm(suspicious_files[:max_pairs], desc="Procesando"):
            txt_file = xml_file.with_suffix('.txt')

            if txt_file.exists():
                self.process_suspicious_document(txt_file, xml_file)
                processed += 1

                # Limitar número de pares
                if len(self.data) >= max_pairs // 2:
                    break

        print(f"Procesados {len(self.data)} pares con plagio")

        # Generar pares negativos (NO plagio)
        self.generate_negative_pairs(num_pairs=len(self.data))

        print(f"\n Total de pares generados: {len(self.data)}")

    def generate_negative_pairs(self, num_pairs: int):
        "Genera pares negativos (sin plagio)."
        print(f"\n Generando {num_pairs} pares sin plagio...")

        # Recolectar archivos fuente y sospechosos
        source_files = []
        suspicious_files = []

        for part_dir in self.source_path.iterdir():
            if part_dir.is_dir():
                source_files.extend(list(part_dir.glob("*.txt")))

        for part_dir in self.suspicious_path.iterdir():
            if part_dir.is_dir():
                suspicious_files.extend(list(part_dir.glob("*.txt")))

        random.seed(42)

        for _ in tqdm(range(num_pairs), desc="Generando negativos"):
            if len(source_files) > 0 and len(suspicious_files) > 0:
                source_file = random.choice(source_files)
                susp_file = random.choice(suspicious_files)

                # Asegurar que son diferentes
                if source_file.stem != susp_file.stem:
                    source_text = self.read_text_file(source_file)
                    susp_text = self.read_text_file(susp_file)

                    if len(source_text) > 50 and len(susp_text) > 50:
                        self.data.append({
                            'text1': source_text,
                            'text2': susp_text,
                            'is_plagiarism': False,
                            'plagiarism_type': 'none'
                        })

    def save_to_csv(self, output_file: str = "../data/training/pan2011_dataset.csv"):
        """Guarda el dataset procesado."""

        if not self.data:
            print("\n No hay datos para guardar")
            return

        df = pd.DataFrame(self.data)

        # Shuffle
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)

        # Crear directorio
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Guardar
        df.to_csv(output_path, index=False)

        print("\n" + "="*70)
        print(" DATASET GUARDADO EXITOSAMENTE")
        print("="*70)
        print(f"\n Archivo: {output_path}")
        print(f"\n Estadísticas:")
        print(f"   Total de pares: {len(df)}")
        print(f"   Con plagio: {df['is_plagiarism'].sum()}")
        print(f"   Sin plagio: {(~df['is_plagiarism']).sum()}")
        print(f"   Balance: {df['is_plagiarism'].sum() / len(df) * 100:.1f}%")

        if 'plagiarism_type' in df.columns:
            print(f"\n   Tipos de plagio detectados:")
            plagiarism_types = df[df['is_plagiarism']
                                  ]['plagiarism_type'].value_counts()
            for ptype, count in plagiarism_types.items():
                print(f"     • {ptype}: {count}")

        print("\n" + "="*70)


def main():
    """Función principal."""

    print("="*70)
    print("PROCESADOR PAN PLAGIARISM CORPUS 2011")
    print("="*70)

    # Ruta al corpus
    corpus_path = "/Users/snvpau/Downloads/PAN-PLAGIARISM/pan-plagiarism-corpus-2011"

    # Verificar que existe
    if not Path(corpus_path).exists():
        print(f"\n Error: No se encuentra el corpus en {corpus_path}")
        print("\n Verifica la ruta o cambia la variable 'corpus_path' en el script")
        return

    print(f"\n📁 Corpus encontrado: {corpus_path}")

    # Preguntar cantidad de pares
    print("\n¿Cuántos pares deseas generar?")
    print("  500  - Rápido (~2 min)")
    print("  1000 - Recomendado (~5 min)")
    print("  2000 - Completo (~10 min)")

    try:
        num_pairs = int(input("\nNúmero de pares: ").strip() or "1000")
    except:
        num_pairs = 1000

    # Procesar
    processor = PAN2011Processor(corpus_path)
    processor.process_all_documents(max_pairs=num_pairs)

    # Guardar
    processor.save_to_csv()

    print("\n🎉 ¡Listo! Ahora puedes entrenar el modelo:")
    print("\n   cd examples")
    print("   python train_model.py")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()

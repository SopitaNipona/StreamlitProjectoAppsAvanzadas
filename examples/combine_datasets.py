import pandas as pd
from pathlib import Path


def combine_datasets():
    "Combina los datasets disponnibles"

    data_dir = Path("../data/training")
    datasets = []
    dataset_info = []

    # Busqueda de todos los csv
    for csv_file in sorted(data_dir.glob("*.csv")):
        if csv_file.name == "combined_dataset.csv":
            continue

        try:
            df = pd.read_csv(csv_file)

            if all(col in df.columns for col in ['text1', 'text2', 'is_plagiarism']):
                datasets.append(df)
                dataset_info.append({
                    'nombre': csv_file.name,
                    'pares': len(df),
                    'plagio': df['is_plagiarism'].sum(),
                    'no plagio': (~df['is_plagiarism']).sum()
                })
                print(f"✓ {csv_file.name}: {len(df)} pares")

        except Exception as e:
            print(f"\n Error con {csv_file.name}: {e}")

    if not datasets:
        print("\n No se encontraron datasets para combinar")
        return None

    # Combinar
    combined = pd.concat(datasets, ignore_index=True)

    # Shuffle
    combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)

    # Guardar
    output_file = data_dir / "combined_dataset.csv"
    combined.to_csv(output_file, index=False)

    print(f"\n✓ Dataset combinado guardado: {output_file}")
    print(f"  Total: {len(combined)} pares ({combined['is_plagiarism'].sum()} plagio, {(~combined['is_plagiarism']).sum()} no plagio)")

    return output_file


if __name__ == "__main__":
    combine_datasets()

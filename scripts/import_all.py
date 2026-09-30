import os
import re
import time
import pandas as pd
from sqlalchemy import create_engine


DB_URL = "postgresql+psycopg2://admin:admin123@postgres:5432/csvdb"


def sanitize_column_name(name):
    """
    Nettoyage des noms de colonnes PostgreSQL
    """
    name = str(name).strip().lower()
    name = name.replace(" ", "_")
    name = re.sub(r"[^\w]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name


def load_csv(file_path):
    """
    Essaie plusieurs encodages automatiquement
    et détecte le séparateur.
    """

    encodings = [
        "utf-8",
        "cp1252",
        "latin1"
    ]

    last_error = None

    for enc in encodings:
        try:
            df = pd.read_csv(
                file_path,
                sep=None,
                engine="python",
                encoding=enc
            )

            print(f"[OK] Encodage détecté : {enc}")
            return df

        except Exception as e:
            last_error = e

    raise last_error


print("Attente du démarrage PostgreSQL...")
time.sleep(10)

engine = create_engine(DB_URL)

csv_dir = "/csv"

for filename in os.listdir(csv_dir):

    if not filename.lower().endswith(".csv"):
        continue

    file_path = os.path.join(csv_dir, filename)

    table_name = os.path.splitext(filename)[0].lower()

    table_name = re.sub(r"[^\w]", "_", table_name)

    print(f"\n=== Import de {filename} ===")

    try:
        df = load_csv(file_path)

        df.columns = [
            sanitize_column_name(col)
            for col in df.columns
        ]

        print(f"Colonnes détectées :")
        print(df.columns.tolist())

        print(f"Nombre de lignes : {len(df)}")

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False,
            method="multi"
        )

        print(f"[OK] Table '{table_name}' créée")

    except Exception as e:
        print(f"[ERREUR] {filename}")
        print(str(e))
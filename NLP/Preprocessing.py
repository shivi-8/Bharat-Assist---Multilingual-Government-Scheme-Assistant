import pandas as pd
import re
import os
import json


# ============================================================
# 1. FILE PATHS
# ============================================================

INPUT_FILE = "data/schemes.csv"

OUTPUT_DIR = "output"

CLEANED_FILE = os.path.join(
    OUTPUT_DIR,
    "schemes_cleaned.csv"
)

CHUNKS_FILE = os.path.join(
    OUTPUT_DIR,
    "bharatassist_chunks.csv"
)

JSON_FILE = os.path.join(
    OUTPUT_DIR,
    "bharatassist_chunks.json"
)


# Create output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 2. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully!")
print("Number of schemes:", len(df))

print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 3. HANDLE MISSING VALUES
# ============================================================

df = df.fillna("")


# ============================================================
# 4. BASIC TEXT PREPROCESSING
# ============================================================

def clean_text(text):

    # Convert everything to string
    text = str(text)

    # Remove leading/trailing spaces
    text = text.strip()

    # Convert multiple spaces/newlines into one space
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary symbols
    # Keep letters, numbers, Indian currency symbol,
    # punctuation and common mathematical symbols.
    text = re.sub(
        r"[^\w\s₹.,:%+\-/()&]",
        " ",
        text,
        flags=re.UNICODE
    )

    # Remove extra spaces again
    text = re.sub(r"\s+", " ", text)

    # Convert to lowercase
    text = text.lower()

    return text.strip()


# ============================================================
# 5. CLEAN IMPORTANT TEXT COLUMNS
# ============================================================

text_columns = [
    "Scheme Name",
    "Eligibility",
    "Benefits",
    "Age",
    "Income",
    "State/Coverage",
    "Category",
    "Application"
]


print("\nCleaning text...")

for column in text_columns:

    if column in df.columns:

        df[column] = df[column].apply(clean_text)


print("Text preprocessing completed!")


# ============================================================
# 6. REMOVE DUPLICATE SCHEMES
# ============================================================

before = len(df)

df = df.drop_duplicates(
    subset=["Scheme Name"]
)

after = len(df)

print("\nDuplicate schemes removed:", before - after)


# ============================================================
# 7. SAVE CLEANED DATASET
# ============================================================

df.to_csv(
    CLEANED_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nCleaned dataset saved:")
print(CLEANED_FILE)


# ============================================================
# 8. CREATE SCHEME CHUNKS
# ============================================================

def create_chunks(row):

    scheme_name = row["Scheme Name"]

    chunks = []


    # --------------------------------------------------------
    # CHUNK 1 — ELIGIBILITY
    # --------------------------------------------------------

    chunks.append({
        "scheme": scheme_name,

        "section": "eligibility",

        "text":
            f"Scheme: {scheme_name}. "
            f"Eligibility: {row['Eligibility']}"
    })


    # --------------------------------------------------------
    # CHUNK 2 — BENEFITS
    # --------------------------------------------------------

    chunks.append({
        "scheme": scheme_name,

        "section": "benefits",

        "text":
            f"Scheme: {scheme_name}. "
            f"Benefits: {row['Benefits']}"
    })


    # --------------------------------------------------------
    # CHUNK 3 — AGE AND INCOME
    # --------------------------------------------------------

    chunks.append({
        "scheme": scheme_name,

        "section": "age_income",

        "text":
            f"Scheme: {scheme_name}. "
            f"Age requirement: {row['Age']}. "
            f"Income requirement: {row['Income']}"
    })


    # --------------------------------------------------------
    # CHUNK 4 — LOCATION AND CATEGORY
    # --------------------------------------------------------

    chunks.append({
        "scheme": scheme_name,

        "section": "coverage_category",

        "text":
            f"Scheme: {scheme_name}. "
            f"State or coverage: {row['State/Coverage']}. "
            f"Category: {row['Category']}"
    })


    # --------------------------------------------------------
    # CHUNK 5 — APPLICATION
    # --------------------------------------------------------

    chunks.append({
        "scheme": scheme_name,

        "section": "application",

        "text":
            f"Scheme: {scheme_name}. "
            f"Application process: {row['Application']}"
    })


    return chunks


# ============================================================
# 9. GENERATE ALL CHUNKS
# ============================================================

print("\nCreating chunks...")

all_chunks = []

for index, row in df.iterrows():

    chunks = create_chunks(row)

    for chunk_number, chunk in enumerate(chunks, start=1):

        all_chunks.append({

            "chunk_id":
                f"{index + 1}_{chunk_number}",

            "scheme":
                chunk["scheme"],

            "section":
                chunk["section"],

            "text":
                chunk["text"]
        })


# Convert to DataFrame

chunks_df = pd.DataFrame(all_chunks)


# ============================================================
# 10. SAVE CHUNKS AS CSV
# ============================================================

chunks_df.to_csv(
    CHUNKS_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nChunk dataset created!")

print("Total chunks:", len(chunks_df))

print("\nSaved at:")
print(CHUNKS_FILE)


# ============================================================
# 11. SAVE CHUNKS AS JSON
# ============================================================

chunks_df.to_json(
    JSON_FILE,
    orient="records",
    force_ascii=False,
    indent=4
)

print("\nJSON file created!")

print(JSON_FILE)


# ============================================================
# 12. DISPLAY SAMPLE CHUNKS
# ============================================================

print("\n==========================================")
print("SAMPLE CHUNKS")
print("==========================================")

for i in range(min(10, len(chunks_df))):

    print("\nChunk ID:",
          chunks_df.iloc[i]["chunk_id"])

    print("Scheme:",
          chunks_df.iloc[i]["scheme"])

    print("Section:",
          chunks_df.iloc[i]["section"])

    print("Text:")
    print(chunks_df.iloc[i]["text"])

    print("------------------------------------------")


# ============================================================
# 13. FINAL SUMMARY
# ============================================================

print("\n==========================================")
print("PERSON 1 DAY 3 COMPLETED")
print("==========================================")

print("Original schemes :", len(df))

print("Total chunks     :", len(chunks_df))

print("Cleaned dataset  :", CLEANED_FILE)

print("CSV chunks       :", CHUNKS_FILE)

print("JSON chunks      :", JSON_FILE)

print("\nThese chunks are now ready for Person 2.")

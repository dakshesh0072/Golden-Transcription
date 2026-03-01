"""
preprocess.py
-------------
Universal transcript cleaner — works for ANY language.
Integrated for project pipeline usage.
"""

import re
import pandas as pd
import unicodedata

MAX_CHARS = 1000


# -------------------------------------------------
# Core Cleaning Logic (UNCHANGED)
# -------------------------------------------------
def clean_transcript(text) -> str:
    if text is None:
        return ""
    try:
        if pd.isna(text):
            return ""
    except Exception:
        pass

    text = str(text).strip()
    if text.lower() == "nan" or text == "":
        return ""

    if len(text) > MAX_CHARS:
        return ""

    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
    text = text.replace('\u00a0', ' ')

    text = re.sub(r'\{[^}]*\}',  '', text)
    text = re.sub(r'\[[^\]]*\]', '', text)
    text = re.sub(r'【[^】]*】',   '', text)

    text = re.sub(r'[「」『』〈〉〔〕《》]', '', text)

    text = re.sub(r'\([^)]*\)',  '', text)
    text = re.sub(r'（[^）]*）', '', text)

    text = re.sub(
        r'(?:^|(?<=[.!?。！？\s]))\s*([^\s:：\n\d][^\s:：\n]*(?:\s+[^\s:：\n]+){0,2})(?<!\d)[:：](?=\s|$)\s*',
        ' ', text
    )

    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    text = re.sub(r'^[\s\?\؟،,\.…\-–—。！？、「]+', '', text)

    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    if len(text) < 2:
        return ""

    return text


# -------------------------------------------------
# Alias for alignment module
# -------------------------------------------------
def normalize(text):
    if not isinstance(text, str):
        return ""

    # 1️⃣ Normalize unicode (important for multilingual text)
    text = unicodedata.normalize("NFKC", text)

    # 2️⃣ Remove leading/trailing spaces
    text = text.strip()

    # 3️⃣ Replace newlines and tabs with space
    text = text.replace("\n", " ").replace("\t", " ")

    # 4️⃣ Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text


# -------------------------------------------------
# DataFrame Preprocessing (for transcripts.csv)
# -------------------------------------------------
def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans option_1 to option_5 columns.
    Overwrites them directly (simpler pipeline).
    """

    option_cols = ['option_1', 'option_2', 'option_3', 'option_4', 'option_5']

    for col in option_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_transcript)

    return df


# -------------------------------------------------
# Optional CLI usage
# -------------------------------------------------
if __name__ == "__main__":
    input_path = "data/transcripts.csv"
    output_path = "data/transcripts_cleaned.csv"

    df = pd.read_csv(input_path)
    df = preprocess_dataframe(df)
    df.to_csv(output_path, index=False)

    print("Preprocessing complete.")
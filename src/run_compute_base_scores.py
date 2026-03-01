import os
import csv
import pandas as pd
from alignment_scoring import compute_alignment_scores
from agreement_scoring import compute_agreement_scores

INPUT_PATH = "data/transcripts.csv"
AUDIO_DIR = "data/audio"
OUTPUT_PATH = "output/base_scores.csv"

OPTION_COLS = [
    "option_1",
    "option_2",
    "option_3",
    "option_4",
    "option_5",
]

def main():

    print("=" * 60)
    print("COMPUTING BASE SCORES (ALIGNMENT + AGREEMENT)")
    print("=" * 60)

    df = pd.read_csv(INPUT_PATH)

    all_alignment = []
    all_agreement = []

    for idx, row in df.iterrows():

        audio_file = os.path.join(AUDIO_DIR, row["audio_file"])

        transcripts = [
            str(row[col]) if pd.notna(row[col]) else ""
            for col in OPTION_COLS
        ]

        # -------- Alignment --------
        whisper_text, alignment_scores = compute_alignment_scores(
            audio_file, transcripts
        )

        # -------- Agreement --------
        agreement_scores = compute_agreement_scores(transcripts)

        all_alignment.append(alignment_scores)
        all_agreement.append(agreement_scores)

        print(f"Processed {idx+1}/{len(df)}")

    # Save raw scores
    for i in range(5):
        df[f"alignment_{i+1}"] = [scores[i] for scores in all_alignment]
        df[f"agreement_{i+1}"] = [scores[i] for scores in all_agreement]

    os.makedirs("output", exist_ok=True)

    df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
        quoting=csv.QUOTE_ALL
    )

    print("\nBase scores saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
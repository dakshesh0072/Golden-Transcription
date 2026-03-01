import os
import requests
import pandas as pd
import numpy as np
import torch
import whisper
from jiwer import wer
from rapidfuzz import fuzz

from preprocess import normalize
from preprocess import clean_transcript

# =====================================================
# CONFIGURATION
# =====================================================

INPUT_EXCEL = "data/Input_Data.xlsx"
AUDIO_FOLDER = "data/audio"
OUTPUT_FOLDER = "output"

TRANSCRIPTS_CSV = "data/transcripts.csv"
FINAL_OUTPUT = "output/final_submission.xlsx"

# -------- SET MANUAL WEIGHTS HERE --------
WEIGHT_ALIGNMENT = 0.74
WEIGHT_AGREEMENT = 0.26

OPTION_COLS = [
    "option_1",
    "option_2",
    "option_3",
    "option_4",
    "option_5",
]

# =====================================================
# CREATE FOLDERS
# =====================================================

os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =====================================================
# STEP 1: LOAD INPUT FILE
# =====================================================

print("\nSTEP 1: Reading Input Excel\n")
df_input = pd.read_excel(INPUT_EXCEL)

# =====================================================
# STEP 2: DOWNLOAD AUDIO + CREATE transcripts.csv
# =====================================================

print("STEP 2: Downloading audio (if needed) & creating transcripts.csv\n")

transcript_rows = []

for idx, row in df_input.iterrows():

    audio_url = row["audio"]
    audio_filename = f"audio_{idx+1:03d}.wav"
    audio_path = os.path.join(AUDIO_FOLDER, audio_filename)

    # Download only if not exists
    if not os.path.exists(audio_path):
        try:
            r = requests.get(audio_url, timeout=30)
            r.raise_for_status()
            with open(audio_path, "wb") as f:
                f.write(r.content)
            print("Downloaded:", audio_filename)
        except Exception as e:
            print("Download failed:", audio_url)
            print(e)
            continue

    transcript_rows.append({
        "audio_id": f"{idx+1:03d}",
        "audio_file": audio_filename,
        "option_1": row["option_1"],
        "option_2": row["option_2"],
        "option_3": row["option_3"],
        "option_4": row["option_4"],
        "option_5": row["option_5"],
    })

transcripts_df = pd.DataFrame(transcript_rows)
transcripts_df.to_csv(TRANSCRIPTS_CSV, index=False)

print("\ntranscripts.csv created.\n")

# =====================================================
# STEP 3: LOAD WHISPER (ONLY ONCE)
# =====================================================

print("STEP 3: Loading Whisper model\n")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Whisper running on:", DEVICE)

model = whisper.load_model("small", device=DEVICE)

alignment_matrix = []
agreement_matrix = []
whisper_texts = []

# =====================================================
# STEP 4: COMPUTE SCORES
# =====================================================

print("\nSTEP 4: Computing alignment + agreement\n")

for idx, row in transcripts_df.iterrows():

    audio_path = os.path.join(AUDIO_FOLDER, row["audio_file"])

    # Whisper transcription
    result = model.transcribe(audio_path, temperature=0.0, beam_size=5)
    whisper_text = normalize(result["text"])
    whisper_texts.append(whisper_text)

    transcripts_alignment = [normalize(str(row[c])) for c in OPTION_COLS]
    transcripts_agreement = [clean_transcript(str(row[c])) for c in OPTION_COLS]

    # ---------- ALIGNMENT ----------
    align_scores = []
    for t in transcripts_alignment:
        error = wer(whisper_text, t)
        wer_sim = max(0.0, 1 - error)
        fuzzy_sim = fuzz.ratio(whisper_text, t) / 100.0
        final_score = 0.6 * wer_sim + 0.4 * fuzzy_sim
        align_scores.append(final_score)

    alignment_matrix.append(align_scores)

    # ---------- AGREEMENT ----------
    agree_scores = []
    for i in range(5):
        pairwise = []
        for j in range(5):
            if i == j:
                continue
            s1 = wer(transcripts_agreement[i], transcripts_agreement[j])
            s2 = wer(transcripts_agreement[j], transcripts_agreement[i])
            pairwise.append((s1 + s2) / 2)

        median_wer = np.median(pairwise)
        agreement_similarity = 1 / (1 + median_wer)
        agree_scores.append(agreement_similarity)

    agreement_matrix.append(agree_scores)

    print(f"Processed {idx+1}/{len(transcripts_df)}")

alignment_matrix = np.array(alignment_matrix)
agreement_matrix = np.array(agreement_matrix)

# =====================================================
# STEP 5: APPLY MANUAL WEIGHTS
# =====================================================

print("\nSTEP 5: Applying manual weights\n")

final_scores = (
    WEIGHT_ALIGNMENT * alignment_matrix +
    WEIGHT_AGREEMENT * agreement_matrix
)

best_options = np.argmax(final_scores, axis=1) + 1

# =====================================================
# STEP 6: GENERATE FINAL SUBMISSION FILE
# =====================================================

print("\nSTEP 6: Generating final submission file (.xlsx)\n")

submission_rows = []

for i in range(len(df_input)):

    transcripts_alignment = [
        normalize(str(df_input.iloc[i][c])) for c in OPTION_COLS
    ]

    whisper_text = whisper_texts[i]

    wer_scores = [
        round(wer(whisper_text, t), 4)
        for t in transcripts_alignment
    ]

    best_option = int(best_options[i])
    golden_transcript = df_input.iloc[i][f"option_{best_option}"]

    submission_rows.append({
        "audio_id": f"{i+1:03d}",
        "language": "auto",
        "audio": df_input.iloc[i]["audio"],
        "option_1": df_input.iloc[i]["option_1"],
        "option_2": df_input.iloc[i]["option_2"],
        "option_3": df_input.iloc[i]["option_3"],
        "option_4": df_input.iloc[i]["option_4"],
        "option_5": df_input.iloc[i]["option_5"],
        "golden_transcript": golden_transcript,
        "best_option": best_option,
        "wer_option1": wer_scores[0],
        "wer_option2": wer_scores[1],
        "wer_option3": wer_scores[2],
        "wer_option4": wer_scores[3],
        "wer_option5": wer_scores[4],
    })

final_df = pd.DataFrame(submission_rows)

with pd.ExcelWriter(FINAL_OUTPUT, engine="openpyxl") as writer:
    final_df.to_excel(writer, index=False, sheet_name="Submission")

print("FINAL FILE SAVED TO:", FINAL_OUTPUT)
print("\nPIPELINE COMPLETED SUCCESSFULLY.\n")
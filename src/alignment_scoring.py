import whisper
import torch
from jiwer import wer
from rapidfuzz import fuzz
from preprocess import normalize   # Reuse your existing normalization

# -------------------------------------------------
# Device Setup
# -------------------------------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Alignment model using device:", DEVICE)

# Use small model for better multilingual accuracy
model = whisper.load_model("small", device=DEVICE)


# -------------------------------------------------
# Transcription (deterministic & multilingual)
# -------------------------------------------------
def get_whisper_transcription(audio_path):
    result = model.transcribe(
        audio_path,
        temperature=0.0,   # removes randomness
        beam_size=5        # stable decoding
    )

    return normalize(result["text"])


# -------------------------------------------------
# Alignment Scoring
# -------------------------------------------------
def compute_alignment_scores(audio_path, transcripts):
    """
    Returns:
        whisper_text (str)
        scores (list of float between 0 and 1)
    """

    whisper_text = get_whisper_transcription(audio_path)

    scores = []

    for t in transcripts:
        t_norm = normalize(t)

        # --- Word-level similarity (strict) ---
        error = wer(whisper_text, t_norm)
        wer_similarity = max(0.0, 1 - error)

        # --- Character-level similarity (soft) ---
        fuzzy_similarity = fuzz.ratio(whisper_text, t_norm) / 100.0

        # --- Hybrid score ---
        final_score = 0.6 * wer_similarity + 0.4 * fuzzy_similarity

        scores.append(round(final_score, 4))

    return whisper_text, scores
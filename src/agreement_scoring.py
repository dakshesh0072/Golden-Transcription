from jiwer import wer
import numpy as np
from preprocess import clean_transcript


def compute_agreement_scores(transcripts):
    """
    transcripts: list of raw transcript options (5 strings)

    returns:
        list of agreement scores (higher = better)
    """

    # Normalize using your project cleaner
    cleaned = [clean_transcript(t) for t in transcripts]

    n = len(cleaned)
    scores = []

    for i in range(n):
        t_i = cleaned[i]

        # Skip empty or too short transcripts
        if not t_i or len(t_i.split()) < 2:
            scores.append(0.0)
            continue

        pairwise_wers = []

        for j in range(n):
            if i == j:
                continue

            t_j = cleaned[j]

            if not t_j or len(t_j.split()) < 2:
                continue

            # Symmetric WER
            score_ij = wer(t_i, t_j)
            score_ji = wer(t_j, t_i)
            symmetric_score = (score_ij + score_ji) / 2

            pairwise_wers.append(symmetric_score)

        if not pairwise_wers:
            scores.append(0.0)
        else:
            # Robust median WER
            median_wer = np.median(pairwise_wers)

            # Convert lower=better → higher=better
            # Stable bounded similarity
            agreement_similarity = 1 / (1 + median_wer)

            scores.append(round(float(agreement_similarity), 4))

    return scores
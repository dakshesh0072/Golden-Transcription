-> README.md

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Project: Golden-Transcription

&nbsp;Important Setup Instructions

1\) Input File Requirement

Before running the project:

•	Rename your input Excel file to:

Input\_Data.xlsx

•	Place it inside the data/ folder.

•	The format and column names must exactly match the original provided Excel file, including:

audio

option\_1

option\_2

option\_3

option\_4

option\_5

Do not change column names or structure.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Python Requirement

This project requires:

Python 3.11.x

-> Do NOT use Python 3.12+ (may cause PyTorch/Whisper compatibility issues)

Check version:

python --version

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Recommended: Create Virtual Environment

python -m venv .venv

.venv\\Scripts\\activate

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Required Libraries

Install GPU-enabled PyTorch first (recommended for speed):

&nbsp;Install PyTorch with CUDA (GPU)

For CUDA 12.4:

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

Official Installation Guide:

-> https://pytorch.org/get-started/locally/

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Then install remaining dependencies:

pip install -r requirements.txt --no-deps

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Libraries Used \& Why

-> torch

•	Core deep learning framework.

•	Used for GPU acceleration.

•	Required for running Whisper.

•	Installed locally (not cloud-based).

-> openai-whisper

•	Automatic Speech Recognition (ASR) model.

•	Downloads the Whisper model locally on your machine during first run.

•	Used for transcribing audio.

•	Repository: https://github.com/openai/whisper

-> jiwer

•	Computes Word Error Rate (WER).

•	Used in:

o	Alignment scoring

o	Agreement scoring

-> rapidfuzz

•	Fast string similarity computation.

•	Used for character-level similarity in alignment scoring.

-> pandas

•	Data processing and Excel/CSV handling.

-> numpy

•	Numerical operations (median computation in agreement scoring).

-> openpyxl

•	Used to generate final .xlsx output file.

-> requests

•	Downloads audio files from URLs.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;How To Run The Project

After setup, simply run:

python src/run\_full\_pipeline.py

That’s it.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Output

After execution, you will find:

output/final\_submission.xlsx

This file contains:

•	All 100 audio entries

•	All transcript options

•	Selected golden\_transcript

•	best\_option

•	WER scores for each option

This is the final required submission file for the project.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Note About Other Files in src/

The following files exist only to support:

optimise\_weights.py

These include:

•	alignment\_scoring.py

•	agreement\_scoring.py

•	run\_compute\_base\_scores.py

They were used during experimentation to:

•	Compute base scores

•	Optimize weights between alignment and agreement

•	Tune parameters

They are not required to generate the final submission file.

Only:

run\_full\_pipeline.py

is required for full execution.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Project Approach

&nbsp;Problem

Given:

•	100 audio files

•	5 transcript options per audio

Goal:

Select the most accurate transcript for each audio file.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Our Approach

We designed a Hybrid Scoring System combining:

1\) Alignment-based scoring

2\) Agreement-based scoring

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

1\) Alignment-Based Scoring

What We Did

•	Used Whisper ASR to transcribe each audio.

•	Compared Whisper transcription against each of the 5 options.

How We Measured Similarity

For each option:

•	Word-level similarity using WER

•	Character-level similarity using RapidFuzz

•	Hybrid alignment score:

Final Alignment Score =

0.6 × WER Similarity +

0.4 × Fuzzy Similarity

Higher score = better match with audio.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

2\) Agreement-Based Scoring

Instead of using audio, we also evaluated:

How consistent each option is with the other 4 options.

Process:

•	Clean transcripts

•	Compute pairwise symmetric WER

•	Take median WER

•	Convert to similarity:

Agreement Score = 1 / (1 + median\_wer)

Higher score = more agreement with others.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Final Hybrid Score

We combine both:

Final Score =

(W\_ALIGNMENT × Alignment Score) +

(W\_AGREEMENT × Agreement Score)

Weights were optimized experimentally.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Final Decision

For each audio:

•	Compute final score for all 5 options

•	Select the option with highest score

•	Mark as:

golden\_transcript

best\_option

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Why This Hybrid Approach?

•	Alignment ensures transcript matches actual speech.

•	Agreement ensures transcript is linguistically consistent.

•	Combining both reduces noise and improves robustness.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Result

On labeled samples:

•	Achieved ~65% accuracy.

•	Fully automated.

•	Fully GPU accelerated.

•	Fully reproducible.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

&nbsp;Final Summary

-> Fully local execution

-> GPU accelerated

-> No external APIs

-> Deterministic transcription

-> Clean modular architecture

-> Single-command execution




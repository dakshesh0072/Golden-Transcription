\#  Golden-Transcription



A fully local, GPU-accelerated hybrid transcription scoring system that selects the most accurate transcript among multiple options using Whisper ASR + hybrid scoring.



---



\#  Important Setup Instructions



\## 1) Input File Requirement



Before running the project:



\- Rename your input Excel file to:



Input\_Data.xlsx





\- Place it inside the `data/` folder.

\- The format and column names must exactly match:



audio

option\_1

option\_2

option\_3

option\_4

option\_5



Do not change column names or structure.



---



\#  Python Requirement



This project requires:



```

Python 3.11.x

```



Do NOT use Python 3.12+ (may cause PyTorch/Whisper compatibility issues).



Check version:



```bash

python --version

```



---



\#  Recommended: Create Virtual Environment



\## Windows



```bash

python -m venv .venv

.venv\\Scripts\\activate

```



\## Mac/Linux



```bash

python -m venv .venv

source .venv/bin/activate

```



---



\#  Required Libraries



\##  Install PyTorch with CUDA (GPU Recommended)



For CUDA 12.4:



```bash

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

```



Official installation guide:  

https://pytorch.org/get-started/locally/



---



\## Install Remaining Dependencies



```bash

pip install openai-whisper

pip install pandas

pip install numpy

pip install jiwer

pip install rapidfuzz

pip install openpyxl

pip install requests

pip install tqdm

```



---



\# Libraries Used \& Why



\##  torch

\- Core deep learning framework

\- Enables GPU acceleration

\- Required for running Whisper

\- Installed locally



\##  openai-whisper

\- Automatic Speech Recognition (ASR) model

\- Downloads Whisper model locally on first run

\- Used for transcribing audio

\- Repository: https://github.com/openai/whisper



\##  jiwer

\- Computes Word Error Rate (WER)

\- Used in:

&nbsp; - Alignment scoring

&nbsp; - Agreement scoring



\## rapidfuzz

\- Fast string similarity computation

\- Used for character-level similarity



\## pandas

\- Data processing

\- Excel/CSV handling



\## numpy

\- Numerical operations

\- Median computation



\## openpyxl

\- Generates final `.xlsx` output file



\## requests

\- Downloads audio files from URLs



---



\# How To Run The Project



After setup, simply run:



```bash

python src/run\_full\_pipeline.py

```



That’s it.



---



\# Output



After execution, you will find:



```

output/final\_submission.xlsx

```



This file contains:



\- All 100 audio entries

\- All transcript options

\- Selected golden\_transcript

\- best\_option

\- WER scores for each option



This is the final required submission file.



---



\# Note About Other Files in `src/`



The following files exist only to support:



```

optimise\_weights.py

```



These include:



\- alignment\_scoring.py

\- agreement\_scoring.py

\- run\_compute\_base\_scores.py



They were used during experimentation to:



\- Compute base scores

\- Optimize weights between alignment and agreement

\- Tune parameters



They are not required to generate the final submission file.



Only:



```

run\_full\_pipeline.py

```



is required for full execution.



---



\# Project Approach



\## Problem



Given:

\- 100 audio files

\- 5 transcript options per audio



Goal:

Select the most accurate transcript for each audio file.



---



\# Our Approach



We designed a Hybrid Scoring System combining:



1\) Alignment-based scoring  

2\) Agreement-based scoring  



---



\## 1) Alignment-Based Scoring



\### What We Did



\- Used Whisper ASR to transcribe each audio

\- Compared Whisper transcription against each of the 5 options



\### Similarity Measurement



For each option:



\- Word-level similarity using WER

\- Character-level similarity using RapidFuzz



Hybrid alignment score:



```

Final Alignment Score =

0.6 × WER Similarity +

0.4 × Fuzzy Similarity

```



Higher score = better match with audio.



---



\## 2) Agreement-Based Scoring



We also evaluated how consistent each option is with the other four options.



\### Process



\- Clean transcripts

\- Compute pairwise symmetric WER

\- Take median WER

\- Convert to similarity:



```

Agreement Score = 1 / (1 + median\_wer)

```



Higher score = more agreement with others.



---



\# ⚖️ Final Hybrid Score



We combine both:



```

Final Score =

(W\_ALIGNMENT × Alignment Score) +

(W\_AGREEMENT × Agreement Score)

```



Weights were optimized experimentally.



---



\# Final Decision



For each audio:



\- Compute final score for all 5 options

\- Select the option with highest score

\- Mark as:

&nbsp; - golden\_transcript

&nbsp; - best\_option



---



\# Why This Hybrid Approach?



\- Alignment ensures transcript matches actual speech

\- Agreement ensures transcript is linguistically consistent

\- Combining both reduces noise

\- Improves robustness



---



\# Result



On labeled samples:



\- ~65% accuracy

\- Fully automated

\- Fully GPU accelerated

\- Fully reproducible



---



\# Final Summary



\- Fully local execution

\- GPU accelerated

\- No external APIs

\- Deterministic transcription

\- Clean modular architecture

\- Single-command execution


import pandas as pd
import numpy as np

BASE_PATH = "output/base_scores.csv"
GROUND_TRUTH_PATH = "data/Input_Data.xlsx"

def main():

    df = pd.read_csv(BASE_PATH)
    gt_df = pd.read_excel(GROUND_TRUTH_PATH)

    gt = pd.to_numeric(gt_df.iloc[:48, 8], errors="coerce").values

    alignment = df[[f"alignment_{i}" for i in range(1,6)]].values
    agreement = df[[f"agreement_{i}" for i in range(1,6)]].values

    train_idx = np.arange(0, 40)
    val_idx = np.arange(40, 48)

    best_acc = 0
    best_weights = (0, 0)

    for w_align in np.arange(0, 1.01, 0.01):
        w_agree = 1 - w_align

        final_scores = w_align * alignment + w_agree * agreement
        best_options = np.argmax(final_scores, axis=1) + 1

        acc = np.mean(best_options[train_idx] == gt[train_idx])

        if acc > best_acc:
            best_acc = acc
            best_weights = (round(w_align, 2), round(w_agree, 2))

    w_align, w_agree = best_weights
    final_scores = w_align * alignment + w_agree * agreement
    best_options = np.argmax(final_scores, axis=1) + 1

    val_acc = np.mean(best_options[val_idx] == gt[val_idx])

    print("Best Weights:", best_weights)
    print("Train Accuracy:", round(best_acc, 4))
    print("Validation Accuracy:", round(val_acc, 4))


if __name__ == "__main__":
    main()
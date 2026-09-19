"""
Downloads the full raw and processed datasets from Google Drive.
Both files are too large for GitHub (>50MB), so they're hosted on
Drive instead and fetched here.

Setup:
    pip install gdown

Usage:
    python data/raw/download_data.py

This saves both files into data/raw/. That path is git-ignored, so
this script is how anyone cloning the repo gets the complete data.
"""

import os
import gdown

# Get each ID from its shareable link:
#   https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
#                                    ^^^^^^^^^^^^ this part
FILES = {
    "processed_dataset.csv": "1Kaphgn-56eF-nP5KbIeRPR9B7DL_3Cez",
    "credit_card_fraud.csv": "PASTE_RAW_DATASET_FILE_ID_HERE",
}

RAW_DIR = os.path.dirname(__file__)


def download():
    for filename, file_id in FILES.items():
        output_path = os.path.join(RAW_DIR, filename)

        if "PASTE_" in file_id:
            print(f"Skipping {filename}: no file ID set yet in FILES dict.")
            continue

        if os.path.exists(output_path):
            print(f"{filename} already exists, skipping download.")
            continue

        url = f"https://drive.google.com/uc?id={file_id}"
        print(f"Downloading {filename} ...")
        gdown.download(url, output_path, quiet=False)

    print("Done.")


if __name__ == "__main__":
    download()

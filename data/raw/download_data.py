"""
Downloads the full raw dataset (credit_card_fraud.csv) from Google Drive.

Setup:
    pip install gdown

Usage:
    python data/raw/download_data.py

This will save the full file to data/raw/credit_card_fraud.csv.
That path is git-ignored, so this script is how anyone cloning the repo
gets the complete data.
"""

import os
import gdown

# TODO: replace with your actual Google Drive file ID
# Get it from your shareable link:
#   https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
#                                    ^^^^^^^^^^^^ this part
FILE_ID = "https://drive.google.com/file/d/1xWQa8i53ktNHb699pdh4i3gzxHfBgeDn/view?usp=drive_link"

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "credit_card_fraud.csv")


def download():
    if os.path.exists(OUTPUT_PATH):
        print(f"File already exists at {OUTPUT_PATH}, skipping download.")
        return

    url = f"https://drive.google.com/uc?id={FILE_ID}"
    print(f"Downloading full dataset to {OUTPUT_PATH} ...")
    gdown.download(url, OUTPUT_PATH, quiet=False)
    print("Done.")


if __name__ == "__main__":
    download()

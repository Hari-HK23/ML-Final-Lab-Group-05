"""
Group 5 – PayShield Fintech
Member 1: Reusable data preprocessing functions
"""

from pathlib import Path
import numpy as np
import pandas as pd


def load_data(file_path):
    """Load the raw CSV dataset."""
    return pd.read_csv(file_path)


def validate_schema(df):
    """Validate that all expected columns are present."""
    expected_columns = {
        "trans_date_trans_time",
        "merchant",
        "category",
        "amt",
        "city",
        "state",
        "lat",
        "long",
        "city_pop",
        "job",
        "dob",
        "trans_num",
        "merch_lat",
        "merch_long",
        "is_fraud",
    }

    missing_columns = expected_columns - set(df.columns)
    unexpected_columns = set(df.columns) - expected_columns

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return {
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
    }


def clean_data(df):
    """Clean text fields, dates and identifiers."""
    df = df.copy()

    for col in ["merchant", "category", "city", "job"]:
        df[col] = df[col].astype("string").str.strip()

    df["category"] = df["category"].str.lower()
    df["state"] = df["state"].astype("string").str.strip().str.upper()

    df["trans_date_trans_time"] = pd.to_datetime(
        df["trans_date_trans_time"], errors="coerce"
    )

    df["dob"] = pd.to_datetime(df["dob"], errors="coerce")

    df = df.drop_duplicates().reset_index(drop=True)

    return df


def validate_values(df):
    """Check domain constraints and return a quality summary."""
    checks = {
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_transaction_ids": int(df["trans_num"].duplicated().sum()),
        "negative_amounts": int((df["amt"] < 0).sum()),
        "invalid_latitude": int(((df["lat"] < -90) | (df["lat"] > 90)).sum()),
        "invalid_longitude": int(((df["long"] < -180) | (df["long"] > 180)).sum()),
        "invalid_merchant_latitude": int(
            ((df["merch_lat"] < -90) | (df["merch_lat"] > 90)).sum()
        ),
        "invalid_merchant_longitude": int(
            ((df["merch_long"] < -180) | (df["merch_long"] > 180)).sum()
        ),
        "negative_city_population": int((df["city_pop"] < 0).sum()),
        "invalid_target_values": int((~df["is_fraud"].isin([0, 1])).sum()),
    }

    return checks


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in kilometres."""
    R = 6371.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )

    return 2 * R * np.arcsin(np.sqrt(a))


def create_features(df):
    """Create Member 1 model features."""
    df = df.copy()

    df["age"] = (
        (df["trans_date_trans_time"] - df["dob"]).dt.days / 365.25
    ).astype("Int64")

    df["hour"] = df["trans_date_trans_time"].dt.hour
    df["day_of_week"] = df["trans_date_trans_time"].dt.dayofweek
    df["month"] = df["trans_date_trans_time"].dt.month

    df["log_amt"] = np.log1p(df["amt"])

    df["distance_km"] = haversine_distance(
        df["lat"],
        df["long"],
        df["merch_lat"],
        df["merch_long"],
    )

    df = df.drop(columns=["trans_num", "dob"])

    return df

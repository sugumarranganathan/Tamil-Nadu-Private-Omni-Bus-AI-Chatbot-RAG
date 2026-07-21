
"""
filter_engine.py
Version 3.0 (Starter Template)

NOTE:
A complete production version is several hundred lines long.
This template preserves the structure and indicates where each
section belongs.
"""

import re
from datetime import datetime

import pandas as pd

from config import DATA_FILE

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip()

# ==========================================================
# Dynamic Master Lists
# ==========================================================

CITIES = sorted(set(df["From_City"].dropna()) | set(df["To_City"].dropna()))
OPERATORS = sorted(df["Operator"].dropna().unique().tolist())
BUS_TYPES = sorted(df["Bus_Type"].dropna().unique().tolist())
BOARDING_POINTS = sorted(df["Boarding_Point"].dropna().unique().tolist())
DROPPING_POINTS = sorted(df["Dropping_Point"].dropna().unique().tolist())
RUNNING_DAYS = sorted(df["Running_Days"].dropna().unique().tolist())

# ==========================================================
# Utility Functions
# ==========================================================

def create_filters():
    return {
        "source": None,
        "destination": None,
        "operator": None,
        "bus_name": None,
        "bus_type": None,
        "boarding": None,
        "dropping": None,
        "min_fare": None,
        "max_fare": None,
        "min_rating": None,
        "max_duration": None,
        "min_available_seats": None,
        "departure_after": None,
        "departure_before": None,
        "arrival_after": None,
        "arrival_before": None,
        "running_day": None,
        "amenities": [],
        "sort_by": None,
        "sort_order": "asc",
    }

def normalize_query(query):
    query = query.lower()
    query = re.sub(r"[₹,]", "", query)
    return re.sub(r"\s+", " ", query).strip()

def time_to_minutes(value):
    if pd.isna(value):
        return None
    for fmt in ("%H:%M", "%I:%M %p", "%H:%M:%S"):
        try:
            t = datetime.strptime(str(value).strip(), fmt)
            return t.hour * 60 + t.minute
        except ValueError:
            pass
    return None

def duration_to_minutes(value):
    try:
        h, m = map(int, str(value).split(":"))
        return h * 60 + m
    except Exception:
        return None

# ==========================================================
# TODO:
# - extract_route()
# - extract_operator()
# - extract_bus_name()
# - extract_bus_type()
# - extract_fare()
# - extract_fare_range()
# - extract_rating()
# - extract_available_seats()
# - extract_departure_time()
# - extract_arrival_time()
# - extract_duration()
# - extract_running_day()
# - extract_amenities()
# - extract_boarding()
# - extract_dropping()
# - extract_time_period()
# - extract_sort()
# - extract_filters()
# - apply_filters()
# - sort_results()
# - filter_dataframe()
#
# These sections should contain the production logic discussed
# during the design process.
# ==========================================================

"""
=========================================================
Advanced Filter Engine
Tamil Nadu Private Omni Bus AI Chatbot (RAG)

Version : 3.0
Author  : Sugumar R
=========================================================
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

CITIES = sorted(
    set(df["From_City"].dropna().unique())
    |
    set(df["To_City"].dropna().unique())
)

OPERATORS = sorted(
    df["Operator"].dropna().unique().tolist()
)

BUS_NAMES = sorted(
    df["Bus_Name"].dropna().unique().tolist()
)

BUS_TYPES = sorted(
    df["Bus_Type"].dropna().unique().tolist()
)

BOARDING_POINTS = sorted(
    df["Boarding_Point"].dropna().unique().tolist()
)

DROPPING_POINTS = sorted(
    df["Dropping_Point"].dropna().unique().tolist()
)

RUNNING_DAYS = sorted(
    df["Running_Days"].dropna().unique().tolist()
)

# ==========================================================
# Dynamic Amenities
# ==========================================================

AMENITIES = set()

for value in df["Amenities"].dropna():

    for amenity in str(value).split(","):

        amenity = amenity.strip()

        if amenity:

            AMENITIES.add(amenity)

AMENITIES = sorted(AMENITIES)

# ==========================================================
# Bus Type Synonyms
# ==========================================================

BUS_TYPE_MAP = {

    "luxury": "Luxury Sleeper",

    "luxury sleeper": "Luxury Sleeper",

    "ac": "AC Sleeper",

    "ac sleeper": "AC Sleeper",

    "non ac": "Non AC Sleeper",

    "non ac sleeper": "Non AC Sleeper",

    "semi": "Semi Sleeper",

    "semi sleeper": "Semi Sleeper",

    "seater": "AC Seater",

    "ac seater": "AC Seater",

    "volvo": "Volvo Multi Axle",

    "multi axle": "Volvo Multi Axle",

    "benz": "BharatBenz Sleeper",

    "bharatbenz": "BharatBenz Sleeper"

}

# ==========================================================
# Amenity Synonyms
# ==========================================================

AMENITY_MAP = {

    "wifi": "WiFi",

    "internet": "WiFi",

    "charging": "Charging",

    "charger": "Charging",

    "usb": "Charging",

    "blanket": "Blanket",

    "pillow": "Pillow",

    "water": "Water",

    "reading light": "Reading Light",

    "light": "Reading Light",

    "luxury seat": "Luxury Seat"

}

# ==========================================================
# Running Day Synonyms
# ==========================================================

RUNNING_DAY_MAP = {

    "daily": "Daily",

    "everyday": "Daily",

    "weekday": "Weekdays",

    "weekdays": "Weekdays",

    "working day": "Weekdays",

    "weekend": "Weekends",

    "weekends": "Weekends",

    "saturday": "Weekends",

    "sunday": "Weekends"

}

# ==========================================================
# Create Filter Dictionary
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

        "sort_order": "asc"

    }

# ==========================================================
# Normalize Query
# ==========================================================

def normalize_query(query):

    query = query.lower()

    query = re.sub(r"[₹,]", "", query)

    query = re.sub(r"\s+", " ", query)

    return query.strip()

# ==========================================================
# Time Utility
# ==========================================================

def time_to_minutes(value):

    if pd.isna(value):

        return None

    value = str(value).strip()

    for fmt in ("%H:%M", "%I:%M %p", "%H:%M:%S"):

        try:

            t = datetime.strptime(value, fmt)

            return t.hour * 60 + t.minute

        except ValueError:

            pass

    return None

# ==========================================================
# Duration Utility
# ==========================================================

def duration_to_minutes(value):

    if pd.isna(value):

        return None

    try:

        h, m = str(value).split(":")

        return int(h) * 60 + int(m)

    except:

        return None

# ==========================================================
# Extract Route
# ==========================================================

def extract_route(query, filters):

    match = re.search(

        r"from\s+(.+?)\s+to\s+(.+?)(?:\s|$)",

        query,

        re.IGNORECASE

    )

    if match:

        filters["source"] = match.group(1).title().strip()

        filters["destination"] = match.group(2).title().strip()

        return

    match = re.search(

        r"([a-zA-Z ]+?)\s+to\s+([a-zA-Z ]+)",

        query,

        re.IGNORECASE

    )

    if match:

        source = match.group(1).title().strip()

        destination = match.group(2).title().strip()

        if source in CITIES:

            filters["source"] = source

        if destination in CITIES:

            filters["destination"] = destination

# ==========================================================
# Extract Operator
# ==========================================================

def extract_operator(query, filters):

    q = query.lower()

    for operator in OPERATORS:

        if operator.lower() in q:

            filters["operator"] = operator

            return

# ==========================================================
# Extract Bus Name
# ==========================================================

def extract_bus_name(query, filters):

    q = query.lower()

    for bus in BUS_NAMES:

        if bus.lower() in q:

            filters["bus_name"] = bus

            return

# ==========================================================
# Extract Bus Type
# ==========================================================

def extract_bus_type(query, filters):

    q = query.lower()

    for key, value in BUS_TYPE_MAP.items():

        if key in q:

            filters["bus_type"] = value

            return


# Module 2

# ==========================================================
# Extract Fare
# ==========================================================

def extract_fare(query, filters):

    q = query.lower()

    m = re.search(
        r"(under|below|less than)\s+(\d+)",
        q
    )

    if m:

        filters["max_fare"] = int(m.group(2))

    m = re.search(
        r"(above|greater than|more than)\s+(\d+)",
        q
    )

    if m:

        filters["min_fare"] = int(m.group(2))


# ==========================================================
# Extract Fare Range
# ==========================================================

def extract_fare_range(query, filters):

    q = query.lower()

    m = re.search(

        r"between\s+(\d+)\s+and\s+(\d+)",

        q

    )

    if m:

        filters["min_fare"] = int(m.group(1))

        filters["max_fare"] = int(m.group(2))


# ==========================================================
# Extract Rating
# ==========================================================

def extract_rating(query, filters):

    q = query.lower()

    m = re.search(

        r"rating\s*(above|greater than)?\s*([0-9.]+)",

        q

    )

    if m:

        filters["min_rating"] = float(m.group(2))


# ==========================================================
# Extract Available Seats
# ==========================================================

def extract_available_seats(query, filters):

    q = query.lower()

    m = re.search(

        r"(available seats|seats)\s*(above|greater than|more than)?\s*(\d+)",

        q

    )

    if m:

        filters["min_available_seats"] = int(m.group(3))


# ==========================================================
# Extract Departure Time
# ==========================================================

def extract_departure_time(query, filters):

    q = query.lower()

    m = re.search(

        r"(after|before)\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?",

        q

    )

    if not m:

        return

    mode = m.group(1)

    hour = int(m.group(2))

    minute = int(m.group(3) or 0)

    ampm = m.group(4)

    if ampm == "pm" and hour != 12:

        hour += 12

    elif ampm == "am" and hour == 12:

        hour = 0

    total = hour * 60 + minute

    if mode == "after":

        filters["departure_after"] = total

    else:

        filters["departure_before"] = total


# ==========================================================
# Extract Arrival Time
# ==========================================================

def extract_arrival_time(query, filters):

    q = query.lower()

    m = re.search(

        r"arrival\s+(after|before)\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?",

        q

    )

    if not m:

        return

    mode = m.group(1)

    hour = int(m.group(2))

    minute = int(m.group(3) or 0)

    ampm = m.group(4)

    if ampm == "pm" and hour != 12:

        hour += 12

    elif ampm == "am" and hour == 12:

        hour = 0

    total = hour * 60 + minute

    if mode == "after":

        filters["arrival_after"] = total

    else:

        filters["arrival_before"] = total


# ==========================================================
# Extract Duration
# ==========================================================

def extract_duration(query, filters):

    q = query.lower()

    m = re.search(

        r"(within|under|less than)\s+(\d+)\s+hour",

        q

    )

    if m:

        filters["max_duration"] = int(m.group(2)) * 60


# ==========================================================
# Extract Running Day
# ==========================================================

def extract_running_day(query, filters):

    q = query.lower()

    for key, value in RUNNING_DAY_MAP.items():

        if key in q:

            filters["running_day"] = value

            return


# ==========================================================
# Extract Amenities
# ==========================================================

def extract_amenities(query, filters):

    q = query.lower()

    for key, value in AMENITY_MAP.items():

        if key in q:

            if value not in filters["amenities"]:

                filters["amenities"].append(value)


# ==========================================================
# Extract Boarding Point
# ==========================================================

def extract_boarding(query, filters):

    q = query.lower()

    for point in BOARDING_POINTS:

        if point.lower() in q:

            filters["boarding"] = point

            return


# ==========================================================
# Extract Dropping Point
# ==========================================================

def extract_dropping(query, filters):

    q = query.lower()

    for point in DROPPING_POINTS:

        if point.lower() in q:

            filters["dropping"] = point

            return


# ==========================================================
# Extract Time Period
# ==========================================================

def extract_time_period(query, filters):

    q = query.lower()

    if "morning" in q:

        filters["departure_after"] = 300
        filters["departure_before"] = 720

    elif "afternoon" in q:

        filters["departure_after"] = 720
        filters["departure_before"] = 1020

    elif "evening" in q:

        filters["departure_after"] = 1020
        filters["departure_before"] = 1260

    elif "night" in q:

        filters["departure_after"] = 1260


# ==========================================================
# Extract Sort Preference
# ==========================================================

def extract_sort(query, filters):

    q = query.lower()

    if any(word in q for word in
           ["cheap", "cheapest", "budget", "lowest fare"]):

        filters["sort_by"] = "Fare"
        filters["sort_order"] = "asc"

    elif any(word in q for word in
             ["best", "top rated", "highest rated"]):

        filters["sort_by"] = "Rating"
        filters["sort_order"] = "desc"

    elif any(word in q for word in
             ["fastest", "shortest duration"]):

        filters["sort_by"] = "Duration"
        filters["sort_order"] = "asc"


# ==========================================================
# Master Filter Extractor
# ==========================================================

def extract_filters(query):

    query = normalize_query(query)

    filters = create_filters()

    extract_route(query, filters)

    extract_operator(query, filters)

    extract_bus_name(query, filters)

    extract_bus_type(query, filters)

    extract_fare(query, filters)

    extract_fare_range(query, filters)

    extract_rating(query, filters)

    extract_available_seats(query, filters)

    extract_departure_time(query, filters)

    extract_arrival_time(query, filters)

    extract_duration(query, filters)

    extract_running_day(query, filters)

    extract_amenities(query, filters)

    extract_boarding(query, filters)

    extract_dropping(query, filters)

    extract_time_period(query, filters)

    extract_sort(query, filters)

    return filters


# Module 3

# ==========================================================
# Apply Filters (Production Version)
# ==========================================================

def apply_filters(filters):

    result = df.copy()

    # ------------------------------------------------------
    # Route
    # ------------------------------------------------------

    if filters["source"]:

        result = result[
            result["From_City"].str.lower()
            ==
            filters["source"].lower()
        ]

    if filters["destination"]:

        result = result[
            result["To_City"].str.lower()
            ==
            filters["destination"].lower()
        ]

    # ------------------------------------------------------
    # Operator
    # ------------------------------------------------------

    if filters["operator"]:

        result = result[
            result["Operator"]
            ==
            filters["operator"]
        ]

    # ------------------------------------------------------
    # Bus Name
    # ------------------------------------------------------

    if filters["bus_name"]:

        result = result[
            result["Bus_Name"]
            ==
            filters["bus_name"]
        ]

    # ------------------------------------------------------
    # Bus Type
    # ------------------------------------------------------

    if filters["bus_type"]:

        result = result[
            result["Bus_Type"]
            ==
            filters["bus_type"]
        ]

    # ------------------------------------------------------
    # Fare
    # ------------------------------------------------------

    if filters["min_fare"] is not None:

        result = result[
            result["Fare"] >= filters["min_fare"]
        ]

    if filters["max_fare"] is not None:

        result = result[
            result["Fare"] <= filters["max_fare"]
        ]

    # ------------------------------------------------------
    # Rating
    # ------------------------------------------------------

    if filters["min_rating"] is not None:

        result = result[
            result["Rating"] >= filters["min_rating"]
        ]

    # ------------------------------------------------------
    # Available Seats
    # ------------------------------------------------------

    if filters["min_available_seats"] is not None:

        result = result[
            result["Available_Seats"]
            >=
            filters["min_available_seats"]
        ]

    # ------------------------------------------------------
    # Running Day
    # ------------------------------------------------------

    if filters["running_day"]:

        result = result[
            result["Running_Days"]
            ==
            filters["running_day"]
        ]

    # ------------------------------------------------------
    # Boarding Point
    # ------------------------------------------------------

    if filters["boarding"]:

        result = result[
            result["Boarding_Point"]
            ==
            filters["boarding"]
        ]

    # ------------------------------------------------------
    # Dropping Point
    # ------------------------------------------------------

    if filters["dropping"]:

        result = result[
            result["Dropping_Point"]
            ==
            filters["dropping"]
        ]

    # ------------------------------------------------------
    # Amenities
    # ------------------------------------------------------

    if filters["amenities"]:

        for amenity in filters["amenities"]:

            result = result[
                result["Amenities"]
                .str.contains(
                    amenity,
                    case=False,
                    na=False
                )
            ]

    # ------------------------------------------------------
    # Departure Time
    # ------------------------------------------------------

    if filters["departure_after"] is not None:

        result = result[
            result["Departure_Time"]
            .apply(time_to_minutes)
            >=
            filters["departure_after"]
        ]

    if filters["departure_before"] is not None:

        result = result[
            result["Departure_Time"]
            .apply(time_to_minutes)
            <=
            filters["departure_before"]
        ]

    # ------------------------------------------------------
    # Arrival Time
    # ------------------------------------------------------

    if filters["arrival_after"] is not None:

        result = result[
            result["Arrival_Time"]
            .apply(time_to_minutes)
            >=
            filters["arrival_after"]
        ]

    if filters["arrival_before"] is not None:

        result = result[
            result["Arrival_Time"]
            .apply(time_to_minutes)
            <=
            filters["arrival_before"]
        ]

    # ------------------------------------------------------
    # Duration
    # ------------------------------------------------------

    if filters["max_duration"] is not None:

        result = result[
            result["Duration"]
            .apply(duration_to_minutes)
            <=
            filters["max_duration"]
        ]

    return result


# ==========================================================
# Smart Sorting
# ==========================================================

def sort_results(result, filters):

    if filters["sort_by"] is None:

        return result

    ascending = filters["sort_order"] == "asc"

    return result.sort_values(

        by=filters["sort_by"],

        ascending=ascending

    )


# ==========================================================
# Main Hybrid Filter
# ==========================================================

def filter_dataframe(query):

    filters = extract_filters(query)

    result = apply_filters(filters)

    result = sort_results(result, filters)

    result = result.reset_index(drop=True)

    return result, filters







"""
=========================================================
Advanced Filter Engine
Tamil Nadu Private Omni Bus AI Chatbot (RAG)
Author : Sugumar R
Version : 2.0
=========================================================
"""

import re
import pandas as pd

from config import DATA_FILE

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(DATA_FILE)

# Clean column names
df.columns = df.columns.str.strip()

# ==========================================================
# Dynamic Master Lists
# ==========================================================

# Cities
CITIES = sorted(
    set(df["From_City"].dropna().unique())
    |
    set(df["To_City"].dropna().unique())
)

# Operators
OPERATORS = sorted(
    df["Operator"].dropna().unique().tolist()
)

# Bus Types
BUS_TYPES = sorted(
    df["Bus_Type"].dropna().unique().tolist()
)

# Boarding Points
BOARDING_POINTS = sorted(
    df["Boarding_Point"].dropna().unique().tolist()
)

# Dropping Points
DROPPING_POINTS = sorted(
    df["Dropping_Point"].dropna().unique().tolist()
)

# Running Days
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

    "semi sleeper": "Semi Sleeper",

    "semi": "Semi Sleeper",

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
# Create Empty Filter Dictionary
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

def normalize_query(query: str) -> str:

    query = query.lower()

    query = re.sub(r"[₹,]", "", query)

    query = re.sub(r"\s+", " ", query)

    return query.strip()



# ==========================================================
# Part 2 – Query Extraction Functions
# Extract Route (Source & Destination)
# ==========================================================

def extract_route(query, filters):

    # Pattern: from Chennai to Madurai
    match = re.search(
        r"from\s+(.+?)\s+to\s+(.+?)(?:\s|$)",
        query,
        re.IGNORECASE
    )

    if match:
        filters["source"] = match.group(1).title().strip()
        filters["destination"] = match.group(2).title().strip()
        return

    # Pattern: Chennai to Madurai
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

    for name in df["Bus_Name"].dropna().unique():

        if str(name).lower() in q:

            filters["bus_name"] = name
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


# ==========================================================
# Extract Fare
# ==========================================================

def extract_fare(query, filters):

    q = query.lower()

    m = re.search(r"(under|below|less than)\s+(\d+)", q)

    if m:

        filters["max_fare"] = int(m.group(2))

    m = re.search(r"(above|greater than|more than)\s+(\d+)", q)

    if m:

        filters["min_fare"] = int(m.group(2))


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
# Extract Seats
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
# Part 3 – Smart Query Parser
# Detect Time Period
# ==========================================================

TIME_PERIODS = {

    "morning": (5, 11),

    "afternoon": (12, 16),

    "evening": (17, 20),

    "night": (21, 23),

    "late night": (0, 4)

}


def extract_time_period(query, filters):

    q = query.lower()

    for key in TIME_PERIODS:

        if key in q:

            filters["departure_period"] = key
            return


# ==========================================================
# Detect Sort Preference
# ==========================================================

def extract_sort(query, filters):

    q = query.lower()

    if any(word in q for word in
           ["cheap","cheapest","budget","lowest fare"]):

        filters["sort_by"] = "Fare"
        filters["sort_order"] = "asc"

    elif any(word in q for word in
             ["best","top rated","highest rated"]):

        filters["sort_by"] = "Rating"
        filters["sort_order"] = "desc"

    elif any(word in q for word in
             ["fastest","shortest duration"]):

        filters["sort_by"] = "Duration"
        filters["sort_order"] = "asc"



# ==========================================================
# Master Filter Extractor
# Extract Everything
# ==========================================================

def extract_filters(query):

    query = normalize_query(query)

    filters = create_filters()

    extract_route(query, filters)

    extract_operator(query, filters)

    extract_bus_name(query, filters)

    extract_bus_type(query, filters)

    extract_fare(query, filters)

    extract_rating(query, filters)

    extract_available_seats(query, filters)

    extract_running_day(query, filters)

    extract_amenities(query, filters)

    extract_boarding(query, filters)

    extract_dropping(query, filters)

    extract_time_period(query, filters)

    extract_sort(query, filters)

    return filters


# ==========================================================
# Apply Filters
# ==========================================================

def apply_filters(filters):

    result = df.copy()

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

    if filters["operator"]:

        result = result[
            result["Operator"]
            ==
            filters["operator"]
        ]

    if filters["bus_name"]:

        result = result[
            result["Bus_Name"]
            ==
            filters["bus_name"]
        ]

    if filters["bus_type"]:

        result = result[
            result["Bus_Type"]
            ==
            filters["bus_type"]
        ]

    if filters["max_fare"] is not None:

        result = result[
            result["Fare"] <= filters["max_fare"]
        ]

    if filters["min_fare"] is not None:

        result = result[
            result["Fare"] >= filters["min_fare"]
        ]

    if filters["min_rating"] is not None:

        result = result[
            result["Rating"] >= filters["min_rating"]
        ]

    if filters["min_available_seats"] is not None:

        result = result[
            result["Available_Seats"]
            >=
            filters["min_available_seats"]
        ]

    if filters["running_day"]:

        result = result[
            result["Running_Days"]
            ==
            filters["running_day"]
        ]

    if filters["boarding"]:

        result = result[
            result["Boarding_Point"]
            ==
            filters["boarding"]
        ]

    if filters["dropping"]:

        result = result[
            result["Dropping_Point"]
            ==
            filters["dropping"]
        ]

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

    return result

# ==========================================================
# Smart Sorting
# Sort Results
# ==========================================================

def sort_results(df_result, filters):

    if filters["sort_by"] is None:

        return df_result

    ascending = filters["sort_order"] == "asc"

    return df_result.sort_values(

        by=filters["sort_by"],

        ascending=ascending

    )

# ==========================================================
# Helper Function
# Hybrid Filter
# ==========================================================

def filter_dataframe(query):

    filters = extract_filters(query)

    result = apply_filters(filters)

    result = sort_results(result, filters)

    return result, filters



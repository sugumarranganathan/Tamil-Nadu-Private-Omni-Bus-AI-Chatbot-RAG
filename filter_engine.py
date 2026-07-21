import re
import pandas as pd


# ----------------------------------------
# Extract filters from user query
# ----------------------------------------

def extract_filters(query: str):
    """
    Extract structured filters from the user's query.
    """

    query = query.lower()

    filters = {
        "source": None,
        "destination": None,
        "operator": None,
        "bus_type": None,
        "max_fare": None
    }

    # -------------------------
    # Route
    # Example:
    # Chennai to Madurai
    # Coimbatore to Salem
    # -------------------------

    route = re.search(r"([a-zA-Z ]+)\s+to\s+([a-zA-Z ]+)", query)

    if route:
        filters["source"] = route.group(1).strip().title()
        filters["destination"] = route.group(2).strip().title()

    # -------------------------
    # Bus Type
    # -------------------------

    bus_types = [
        "ac",
        "non ac",
        "sleeper",
        "semi sleeper",
        "volvo",
        "seater"
    ]

    for bt in bus_types:
        if bt in query:
            filters["bus_type"] = bt.title()
            break

    # -------------------------
    # Fare
    # Examples:
    # under 1000
    # below 800
    # less than 1200
    # -------------------------

    fare = re.search(
        r"(under|below|less than)\s*(\d+)",
        query
    )

    if fare:
        filters["max_fare"] = int(fare.group(2))

    return filters


# ----------------------------------------
# Apply filters
# ----------------------------------------

def apply_filters(df: pd.DataFrame, filters: dict):

    results = df.copy()

    if filters["source"]:
        results = results[
            results["Source"].str.lower()
            == filters["source"].lower()
        ]

    if filters["destination"]:
        results = results[
            results["Destination"].str.lower()
            == filters["destination"].lower()
        ]

    if filters["bus_type"]:
        results = results[
            results["BusType"]
            .str.lower()
            .str.contains(filters["bus_type"].lower(), na=False)
        ]

    if filters["operator"]:
        results = results[
            results["Operator"]
            .str.lower()
            .str.contains(filters["operator"].lower(), na=False)
        ]

    if filters["max_fare"] is not None:
        results = results[
            results["Fare"] <= filters["max_fare"]
        ]

    return results.reset_index(drop=True)

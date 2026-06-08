import pandas as pd

df = pd.read_csv("spacez_reviews_dataset.csv", sep="\t")

def normalize_rating(row):
    if row["rating_scale"] == 10:
        return row["rating_raw"] / 2
    return row["rating_raw"]

df["rating_normalized"] = df.apply(
    normalize_rating,
    axis=1
)

print(
    df[
        [
            "platform",
            "rating_raw",
            "rating_scale",
            "rating_normalized"
        ]
    ].head(10)
)

print("\nProperties:")
print(df["property_name"].unique())

low_reviews = df[
    df["rating_normalized"] <= 3
]

print(
    low_reviews[
        [
            "property_name",
            "caretaker_name",
            "rating_normalized",
            "review_text"
        ]
    ]
)

def classify_issue(text):
    text = str(text).lower()

    if "pool" in text:
        return "Pool"

    elif "clean" in text or "dirty" in text:
        return "Cleanliness"

    elif "check-in" in text:
        return "Check-In"

    elif "wifi" in text:
        return "Wifi"

    elif "heating" in text or "hot water" in text:
        return "Heating"

    elif "road" in text:
        return "Road Access"

    return "Other"

df["issue"] = df["review_text"].apply(
    classify_issue
)

print(
    df["issue"].value_counts()
)

print(
    df.groupby(
        ["property_name", "issue"]
    )
    .size()
    .reset_index(name="count")
    .sort_values(
        "count",
        ascending=False
    )
)

print(
    df.groupby(
        ["caretaker_name", "issue"]
    )
    .size()
    .reset_index(name="count")
    .sort_values(
        "count",
        ascending=False
    )
)
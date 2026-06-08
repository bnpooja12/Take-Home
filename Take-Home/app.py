import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.write("Files in directory:")
st.write(os.listdir("."))
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Spacez Review Intelligence Dashboard",
    layout="wide"
)

st.title("🏡 Spacez Review Intelligence Dashboard")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv(
    "spacez_reviews_dataset.csv",
    sep="\t"
)

# --------------------------------------------------
# NORMALIZE RATINGS
# --------------------------------------------------
def normalize_rating(row):
    if row["rating_scale"] == 10:
        return row["rating_raw"] / 2
    return row["rating_raw"]

df["rating_normalized"] = df.apply(
    normalize_rating,
    axis=1
)

# --------------------------------------------------
# ISSUE CLASSIFICATION
# --------------------------------------------------
def classify_issue(text):

    text = str(text).lower()

    if "pool" in text:
        return "Pool"

    elif (
        "clean" in text
        or "dirty" in text
        or "dust" in text
    ):
        return "Cleanliness"

    elif (
        "check-in" in text
        or "check in" in text
        or "checkin" in text
    ):
        return "Check-In"

    elif (
        "wifi" in text
        or "wi-fi" in text
        or "internet" in text
    ):
        return "WiFi"

    elif (
        "heating" in text
        or "hot water" in text
        or "heater" in text
    ):
        return "Heating"

    elif (
        "road" in text
        or "access road" in text
    ):
        return "Road Access"

    return "Other"

df["issue"] = df["review_text"].apply(
    classify_issue
)

# --------------------------------------------------
# ISSUE OWNERSHIP
# --------------------------------------------------
def assign_owner(issue):

    if issue == "Check-In":
        return "Caretaker"

    elif issue in [
        "Pool",
        "Heating",
        "Cleanliness"
    ]:
        return "Operations"

    elif issue in [
        "WiFi",
        "Road Access"
    ]:
        return "External"

    return "Other"

df["owner"] = df["issue"].apply(
    assign_owner
)

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------
negative_reviews = len(
    df[df["rating_normalized"] <= 3]
)

st.subheader("Operations Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Reviews",
    len(df)
)

col2.metric(
    "Properties",
    df["property_name"].nunique()
)

col3.metric(
    "Caretakers",
    df["caretaker_name"].nunique()
)

col4.metric(
    "Average Rating",
    round(
        df["rating_normalized"].mean(),
        2
    )
)

col5.metric(
    "Low Ratings",
    negative_reviews
)

# --------------------------------------------------
# RECURRING ISSUES
# --------------------------------------------------
st.subheader("Recurring Issues")

issue_counts = (
    df[df["issue"] != "Other"]["issue"]
    .value_counts()
    .reset_index()
)

issue_counts.columns = [
    "Issue",
    "Count"
]

fig = px.bar(
    issue_counts,
    x="Issue",
    y="Count",
    title="Recurring Issues Across All Reviews"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# ISSUES BY PROPERTY
# --------------------------------------------------
st.subheader("Issues by Property")

property_issues = (
    df[df["issue"] != "Other"]
    .groupby(
        ["property_name", "issue"]
    )
    .size()
    .reset_index(name="count")
)

fig = px.bar(
    property_issues,
    x="property_name",
    y="count",
    color="issue",
    title="Issue Distribution by Property"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# ISSUES BY CARETAKER
# --------------------------------------------------
st.subheader("Issues by Caretaker")

caretaker_issues = (
    df[df["issue"] != "Other"]
    .groupby(
        ["caretaker_name", "issue"]
    )
    .size()
    .reset_index(name="count")
)

fig = px.bar(
    caretaker_issues,
    x="caretaker_name",
    y="count",
    color="issue",
    title="Issue Distribution by Caretaker"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# ISSUE OWNERSHIP SUMMARY
# --------------------------------------------------
st.subheader("Issue Ownership")

ownership = (
    df["owner"]
    .value_counts()
    .reset_index()
)

ownership.columns = [
    "Owner",
    "Count"
]

st.dataframe(
    ownership,
    use_container_width=True
)

# --------------------------------------------------
# KEY INSIGHTS
# --------------------------------------------------
st.subheader("Key Insights")

st.success(
    """
• Serenity Villa shows recurring pool complaints (5 reviews).

• Vineyard Villa has repeated cleanliness concerns (4 reviews).

• Cliffside Retreat has recurring heating failures (3 reviews).

• Lokesh Gowda's check-in complaints occur across multiple properties,
  suggesting a caretaker process issue rather than a property issue.

• Road access and WiFi complaints should not be attributed directly
  to caretakers.

• Ratings from different platforms were normalized before analysis
  to ensure fair comparison.
"""
)

# --------------------------------------------------
# RECOMMENDED ACTIONS
# --------------------------------------------------
st.subheader("Recommended Actions")

actions = {
    "Pool": "Schedule pool maintenance audit",
    "Cleanliness": "Audit housekeeping vendor",
    "Heating": "Inspect heating systems",
    "Check-In": "Review caretaker arrival process",
    "WiFi": "Escalate issue to ISP/provider"
}

for issue, action in actions.items():
    st.write(
        f"• **{issue}** → {action}"
    )

# --------------------------------------------------
# CRITICAL REVIEWS
# --------------------------------------------------
st.subheader("Critical Reviews")

critical_reviews = df[
    df["rating_normalized"] <= 3
]

st.dataframe(
    critical_reviews[
        [
            "property_name",
            "caretaker_name",
            "rating_normalized",
            "issue",
            "review_text"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# RAW DATA (OPTIONAL)
# --------------------------------------------------
with st.expander("View Raw Dataset"):
    st.dataframe(
        df,
        use_container_width=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")

st.caption(
    "Built for the Spacez AI Product Associate Assignment. "
    "Ratings are normalized across platforms and review issues are "
    "classified into ownership categories to support operational decisions."
)

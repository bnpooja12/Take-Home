# 🏡 Spacez Review Intelligence Dashboard

> **AI-powered review analysis for premium villa operations** — built as part of the Spacez AI Product Associate take-home assignment.

---

## What This Is

A working prototype that ingests 46 cross-platform guest reviews (Airbnb, Booking.com, Google) and transforms them into **actionable intelligence for Operations teams** — the stakeholder I chose to build for, and why.

---

## Why Operations (Not Caretakers or Business)

Three teams care about reviews. One needed the prototype most urgently.

| Stakeholder | What they need | Why I didn't build for them first |
|---|---|---|
| **Business** | Portfolio-level signals, pricing, drop/back decisions | Needs time-series data; 46 reviews is too thin for statistical confidence |
| **Caretakers** | Feedback on their own hosted bookings | *See caretaker risk section below* — this is more complex than it looks |
| **Operations** ✅ | Recurring fixable issues, triage, vendor accountability | Immediate ROI; issues are actionable today; data is sufficient |

Operations can act on a single bad review. Business and Caretaker views compound value over time — they're V2.

---

## The Caretaker Hypothesis — My Pushback

The brief asks: *"Caretakers should get reports on reviews from bookings they hosted. Good idea or risky?"*

**It's risky without careful design**, for three reasons I found in the data:

1. **Many issues aren't caretaker-owned.** Bad road access, WiFi failures from the ISP, misleading listing photos, gate/occupancy policies — these show up in negative reviews but are Operations or Business failures, not Lokesh Gowda's fault. A raw review dump to a caretaker is noise at best, demoralising at worst.

2. **One caretaker covers multiple properties.** Lokesh Gowda manages both Misty Estate and Coorg Canopy. His check-in delays appear across *both* properties — that's a caretaker process failure, not a property problem. The system needs to separate these before surfacing anything to him.

3. **Framing matters enormously.** Showing a caretaker "you got 2/5 on check-in, here are the reviews" without context could damage trust or cause defensiveness. The right framing is coaching, not scoring — *here's a pattern, here's how to fix it.*

**What I'd validate first:** Run a 2-week pilot with one caretaker (ideally Biju Thomas, who has the fewest issues). Share only caretaker-attributable issues, with explicit "not your fault" callouts for external factors. Measure: does it change behaviour? Does it affect caretaker retention?

---

## What the Prototype Does

Built as a **Streamlit dashboard** using the provided dataset with these analytical layers:

### Operations Overview
- Total reviews, unique properties, caretakers, average normalised rating, low-rating count
- Ratings normalised across platforms (Booking.com /10 → /5, Airbnb & Google /5 as-is)

### Recurring Issues Detection
- Bar chart of issue frequency across all reviews
- Top issues: **Pool, Heating, Cleanliness, Check-In, WiFi** (5 occurrences each at the top)

### Issue Distribution by Property
- Stacked bar: which properties have which problem types
- Serenity Villa → Pool (5 reviews), Vineyard Villa → Cleanliness (4), Cliffside Retreat → Heating (3-4)

### Issue Distribution by Caretaker
- Stacked bar: issue patterns per caretaker
- Lokesh Gowda has the most diverse issue set (Check-In + Road Access + Other) across two properties

### Flagged Low-Rating Reviews
- Filterable table of reviews with rating ≤ 3, showing property, caretaker, issue, and full review text
- Sortable for triage

### Issue Ownership Classification
- Each issue tagged: `Operations` (fixable internally), `External` (ISP, road authority), `Caretaker` (process/behaviour), `Other` (listing accuracy, policy)
- Prevents misattribution before any escalation

### Key Insights (AI-generated)
- Serenity Villa: recurring pool complaints (5 reviews) — schedule maintenance audit
- Vineyard Villa: repeated cleanliness concerns (4 reviews) — audit housekeeping vendor
- Cliffside Retreat: recurring heating failures — inspect heating systems before winter season
- Lokesh Gowda's check-in issues span two properties → caretaker process issue, not venue-specific
- Road access and WiFi complaints excluded from caretaker performance scoring

### Recommended Actions
| Issue | Action |
|---|---|
| Pool | Schedule pool maintenance audit |
| Cleanliness | Audit housekeeping vendor |
| Heating | Inspect heating systems |
| Check-In | Review caretaker arrival process |
| WiFi | Escalate to ISP/provider |

---

## Key Design Decisions

**Normalisation before analysis.** Booking.com uses a /10 scale; Airbnb and Google use /5. Blind-averaging these inflates Booking.com scores. All ratings are halved to /5 before any metric is computed.

**"Other" is not a dustbin.** Reviews tagged "Other" include occupancy-policy disputes and listing-accuracy complaints — real problems, but not hospitality failures. The dashboard surfaces them separately rather than burying them.

**Issue ownership is explicit.** The classifier tags each issue with an owner (Operations / External / Caretaker / Other) so the Operations team knows immediately who needs to act — and equally importantly, who *doesn't.*

**Recurring vs. one-off.** A single WiFi complaint might be a bad day. Four cleanliness complaints at the same property from four different guests is a vendor problem. The dashboard counts recurrence to distinguish noise from signal.

---

## Data & Methodology

- **Dataset:** 46 synthetic reviews across 7 properties, 6 caretakers
- **Platforms:** Airbnb, Booking.com, Google
- **Preprocessing:** Rating normalisation, manual issue labeling (Pool, Heating, Cleanliness, Check-In, WiFi, Road Access, Other), issue ownership classification
- **No pre-computed sentiment** — themes were derived from review text, not inherited from the dataset

---

## How I'd Measure Success

**Short-term (1–4 weeks)**
- Time-to-triage: how quickly does Operations action a flagged issue after it appears?
- Issue recurrence rate: does the same issue appear again in the next review cycle?

**Medium-term (1–3 months)**
- Average rating trend per property after intervention
- Vendor audit completion rate (cleanliness, pool maintenance)

**Long-term**
- Reduction in sub-3 ratings as a share of total reviews
- Caretaker NPS if/when the caretaker view is rolled out

---

## What I'd Build Next

1. **Live platform ingestion** — pull from Airbnb/Booking.com/Google APIs instead of manual CSV uploads
2. **Business view** — portfolio-level trends, property-level ROI estimates, drop/back signals
3. **Caretaker view (V2)** — coaching dashboard with only attributable issues, context-stripped language, and a "this wasn't your fault" section for external factors
4. **Alert system** — Slack/email notification when a property accumulates 3+ same-issue reviews in 30 days
5. **LLM-powered summarisation** — auto-generate the insight bullets instead of hardcoding them

---

## Stack

- Python · Pandas · Streamlit · Plotly
- Dataset: provided CSV (46 reviews, extended with `issue` and `issue_owner` labels)

---

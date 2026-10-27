
# BranchPulse — Five-Minute Product Demo

## Purpose

Demonstrate the current BranchPulse prototype to potential users and gather feedback about their existing incident-management and technology-investment decision processes.

**Important:** All included incident records are synthetic. Financial impact and savings are estimates based on assumptions, not verified business outcomes.

## Before the Demo

1. Start BranchPulse using:

   ```powershell
   python -m streamlit run app.py
   ```

2. Confirm that all dashboard tabs load.
3. Confirm that `data/sample_incidents.csv` contains valid sample data.
4. Run the automated tests:

   ```powershell
   python -m pytest -v
   ```

5. Keep the sample data unchanged during the demonstration.

## Opening — 30 Seconds

Say:

"BranchPulse is an early-stage prototype exploring how multi-location businesses could connect technology incidents with financial impact and investment decisions.

The idea is to make it easier to investigate where problems occur, estimate their potential consequences, and compare possible improvements.

The current version uses synthetic data, so today's demonstration shows how the workflow operates rather than proving actual savings."

## Part 1 — Explore Incidents

**Dashboard tab:** Incident Explorer

Show the incident records and explain that each record contains a date, branch, incident type, duration, transaction assumptions, assumed lost-transaction fraction, and recovery cost.

Show the branch and incident-type filters.

Demonstrate selecting Branch A only.

Explain that the current sample contains three incidents for Branch A, with approximately €614.41 in estimated combined impact.

Then restore all filters.

**Business point:** Incident frequency and estimated financial impact are different measures. Two branches can experience the same number of incidents but have different estimated costs.

## Part 2 — Compare Branches and Trends

Show the estimated-impact chart, incident-frequency comparison, and weekly trends.

Explain that these are summaries of the current sample dataset. The charts do not establish long-term patterns because the dataset is small and synthetic.

Ask the audience to consider how they currently compare incidents across properties.

## Part 3 — Explore an Investment Decision

**Dashboard tab:** Investment Planner

Keep the default sample settings:

- Branch: All branches
- Observation period: 3 September 2026 to 19 October 2026
- Assumed preventable fraction: 25%
- Upfront investment cost: €5,000
- Annual maintenance cost: €500

Show the observed estimated impact and the annualized gross-savings estimate.

Explain that the 25% preventable fraction is an assumption chosen by the user. It is not a measured probability that a technology improvement will prevent 25% of the impact.

Show how the conservative, expected, and optimistic scenarios produce different financial outcomes.

Point out the payback and first-year ROI figures, including the possibility that a decision may look attractive under one scenario but less attractive under another.

## Part 4 — Export the Report

Download the investment scenario CSV.

Show that the report includes the date range, selected branch, observed estimated impact, preventable fraction, upfront cost, maintenance cost, scenario results, payback, and ROI.

Explain that the report is intended to make the calculations and their assumptions easier to review.

## Closing — 30 Seconds

Say:

"This prototype brings together incident analysis, financial estimates, investment comparisons, and scenario reporting. I'm currently investigating whether this workflow addresses a real problem for multi-location businesses.

I'd like to understand how your organisation handles these decisions today, what works well, and where the process could be improved."

## Feedback Questions

Ask the interviewee:

1. How do you currently record and compare incidents across locations?
2. How do you estimate the business impact of a technology disruption?
3. What evidence do you need before approving a technology investment?
4. Which assumptions or outputs in this prototype would you challenge?
5. What is missing from the workflow compared with how your organisation actually operates?
6. Does your existing process already solve this problem adequately?

Record critical feedback and contradictory evidence, not only positive reactions.

## Demo Limitations

- The incident data is synthetic.
- Estimated impact is not verified financial loss.
- Preventable impact is an assumed scenario.
- Annualized savings depend on the observation period and an assumption that the incident rate continues.
- The prototype does not establish that any investment will achieve the projected savings.
- No customer validation should be claimed until research has actually been conducted.

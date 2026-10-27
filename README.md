
# BranchPulse

**Turning technology reliability incidents into financial insights and investment decisions.**

BranchPulse is an early-stage decision-support prototype that helps small, multi-location businesses examine the estimated financial impact of technology incidents and evaluate potential technology investments.

Instead of looking at outages only as technical problems, BranchPulse explores how incident duration, transaction assumptions, recovery costs, investment costs, and potential savings can inform business decisions.

## The Business Problem

A business may experience recurring Wi-Fi, internet, DNS, or payment-connectivity issues without having a clear, consistent way to:

- Estimate the potential financial impact of incidents.
- Compare incident frequency with estimated financial impact.
- Identify branches and incident types that deserve further investigation.
- Compare proposed technology investments using payback, return on investment (ROI), and annual net benefit.
- Understand how different savings assumptions affect an investment decision.

BranchPulse explores a transparent, assumption-driven approach to these decisions.

## Current Features

### 1. Business Impact Calculator

Estimate potential lost contribution and recovery costs using incident frequency, duration, transaction volume, contribution per transaction, and an assumed lost-transaction fraction.

### 2. Investment Analysis

Evaluate an investment using upfront cost, expected annual gross savings, and annual maintenance costs. Calculate annual net benefit, estimated payback period, and first-year ROI.

### 3. Investment Comparison

Compare multiple investment options and prioritise them against an optional upfront budget. Review different leading options for annual net benefit, first-year ROI, and payback.

### 4. Savings Sensitivity Analysis

Compare conservative, expected, and optimistic savings scenarios to understand how assumptions can change investment outcomes.

### 5. Incident Explorer

Load incident records from a CSV file and explore estimated impact by branch and incident type. Filter incidents, compare frequency with estimated impact, and view weekly trends.

### 6. Investment Planner

Select a branch and observation period, estimate potentially preventable incident impact, annualise the estimate, and evaluate a proposed investment. Compare conservative, expected, and optimistic preventable-impact assumptions.

### 7. Incident Data Validation

Check incident records for missing required columns, duplicate incident IDs, invalid dates, missing values, negative numerical inputs, and invalid lost-transaction fractions before calculating their estimated impact.

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- pytest

## Project Structure

```text
BranchPulse/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_incidents.csv
├── src/
│   ├── business_calculations.py
│   └── incident_data.py
└── tests/
    ├── test_business_calculations.py
    └── test_incident_data.py
```

The `.venv/` environment and other local development files are not part of the application source.

## Getting Started

### Prerequisites

- Python 3.11
- Git (optional, for version control)

### Run on Windows using PowerShell

Open a terminal in the project folder.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Launch the dashboard:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

### Run the automated tests

With the virtual environment activated, run:

```powershell
python -m pytest -v
```

The project currently has 27 automated tests covering financial calculations, investment comparisons, savings scenarios, preventable-impact estimates, and incident-data validation.

## How the Financial Estimates Work

### Estimated incident impact

The prototype estimates incident impact using:

`Estimated impact = Estimated lost contribution + Recovery cost`

Where:

`Estimated lost contribution = Duration × Transactions per hour × Contribution per transaction × Assumed lost-transaction fraction`

### Investment evaluation

The prototype calculates:

`Annual net benefit = Expected annual gross savings − Annual maintenance cost`

`Estimated payback (months) = Upfront cost ÷ Annual net benefit × 12`

Payback is reported only when annual net benefit is positive.

`First-year ROI = (Annual net benefit − Upfront cost) ÷ Upfront cost × 100`

### Preventable impact

The Investment Planner applies a user-selected preventable fraction to estimated incident impact and annualises it using the number of days in the observation period.

The annualised result assumes that the observed incident rate continues throughout the year. It should be treated cautiously, especially when the observation period is short or the data is incomplete.

## Data and Limitations

- The included incident dataset is synthetic and intended for demonstration.
- Estimated incident impact is not confirmed revenue loss or accounting loss.
- The preventable fraction is a scenario assumption, not a measured probability.
- Annualised savings are projections based on the selected observation period and assumptions.
- Investment comparisons do not independently verify vendor quotes, operational feasibility, future savings, or ongoing affordability.
- The project has not yet established customer validation or demonstrated production performance.

BranchPulse is a prototype for exploring decisions, not a substitute for verified financial data, operational assessment, or professional advice.

## Current Development Status

The project includes a working Streamlit dashboard, reusable financial calculation functions, CSV-based incident analysis, input validation, and automated tests.

Planned improvements include strengthening edge-case handling, improving the investment decision workflow, documenting the architecture, researching competing tools, gathering user feedback, and preparing a portfolio demonstration.

## Project Objective

Explore whether transparent financial modelling and incident analysis can help small, multi-location businesses make better-informed technology investment decisions.

import math

def estimate_annual_impact(
    outages_per_year: int,
    average_duration_hours: float,
    affected_transactions_per_hour: float,
    contribution_per_transaction: float,
    lost_transaction_fraction: float,
    recovery_cost_per_outage: float,
) -> dict[str, float]:
    """Estimate annual financial impact using explicit assumptions."""

    values = {
        "Outages per year": outages_per_year,
        "Outage duration": average_duration_hours,
        "Affected transactions per hour": affected_transactions_per_hour,
        "Contribution per transaction": contribution_per_transaction,
        "Lost transaction fraction": lost_transaction_fraction,
        "Recovery cost per outage": recovery_cost_per_outage,
    }

    for label, value in values.items():
        if not math.isfinite(value):
            raise ValueError(f"{label} must be a finite number.")

    if outages_per_year < 0:
        raise ValueError("Outages per year cannot be negative.")

    if average_duration_hours < 0:
        raise ValueError("Outage duration cannot be negative.")

    if affected_transactions_per_hour < 0:
        raise ValueError("Affected transactions cannot be negative.")

    if contribution_per_transaction < 0:
        raise ValueError("Contribution per transaction cannot be negative.")

    if recovery_cost_per_outage < 0:
        raise ValueError("Recovery cost cannot be negative.")

    if not 0 <= lost_transaction_fraction <= 1:
        raise ValueError("Lost transaction fraction must be between 0 and 1.")

    estimated_lost_transactions = (
        outages_per_year
        * average_duration_hours
        * affected_transactions_per_hour
        * lost_transaction_fraction
    )

    lost_contribution = (
        estimated_lost_transactions * contribution_per_transaction
    )

    annual_recovery_cost = outages_per_year * recovery_cost_per_outage

    total_annual_impact = lost_contribution + annual_recovery_cost

    return {
        "estimated_lost_transactions": estimated_lost_transactions,
        "lost_contribution": lost_contribution,
        "annual_recovery_cost": annual_recovery_cost,
        "total_annual_impact": total_annual_impact,
    }


def estimate_investment_return(
    upfront_cost: float,
    expected_annual_gross_savings: float,
    annual_maintenance_cost: float,
) -> dict[str, float | None]:
    """Estimate the financial return of a proposed technology investment."""

    values = {
        "Upfront cost": upfront_cost,
        "Expected annual savings": expected_annual_gross_savings,
        "Annual maintenance cost": annual_maintenance_cost,
    }

    for label, value in values.items():
        if not math.isfinite(value):
            raise ValueError(f"{label} must be a finite number.")

    if upfront_cost <= 0:
        raise ValueError("Upfront cost must be greater than zero.")

    if expected_annual_gross_savings < 0:
        raise ValueError("Expected annual savings cannot be negative.")

    if annual_maintenance_cost < 0:
        raise ValueError("Annual maintenance cost cannot be negative.")

    annual_net_benefit = (
        expected_annual_gross_savings - annual_maintenance_cost
    )

    if annual_net_benefit > 0:
        payback_months = (upfront_cost / annual_net_benefit) * 12
    else:
        payback_months = None

    first_year_net_benefit = annual_net_benefit - upfront_cost

    first_year_roi_percent = (
        first_year_net_benefit / upfront_cost
    ) * 100

    return {
        "annual_net_benefit": annual_net_benefit,
        "payback_months": payback_months,
        "first_year_roi_percent": first_year_roi_percent,
    }


def compare_investments(
    investments: list[dict[str, str | float]],
    available_budget: float | None = None,
) -> list[dict[str, str | float | bool | None]]:
    """Compare investments and prioritise affordable options when a budget is set."""

    if not investments:
        raise ValueError("At least one investment option is required.")

    if available_budget is not None:
        if not math.isfinite(available_budget):
            raise ValueError("Available budget must be a finite number.")

        if available_budget < 0:
            raise ValueError("Available budget cannot be negative.")
    results = []

    for investment in investments:
        name = investment.get("name", "")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Every investment must have a name.")

        required_fields = (
            "upfront_cost",
            "expected_annual_gross_savings",
            "annual_maintenance_cost",
        )

        missing_fields = [
            field for field in required_fields if field not in investment
        ]

        if missing_fields:
            raise ValueError(
                f"Investment '{name}' is missing: "
                f"{', '.join(missing_fields)}"
            )

        upfront_cost = float(investment["upfront_cost"])

        financial_results = estimate_investment_return(
            upfront_cost=upfront_cost,
            expected_annual_gross_savings=float(
                investment["expected_annual_gross_savings"]
            ),
            annual_maintenance_cost=float(
                investment["annual_maintenance_cost"]
            ),
        )

        within_budget = (
            None
            if available_budget is None
            else upfront_cost <= available_budget
        )

        results.append({
            "name": name.strip(),
            "within_budget": within_budget,
            **financial_results,
        })

    if available_budget is not None:
        return sorted(
            results,
            key=lambda option: (
                bool(option["within_budget"]),
                float(option["annual_net_benefit"]),
            ),
            reverse=True,
        )

    return sorted(
        results,
        key=lambda option: float(option["annual_net_benefit"]),
        reverse=True,
    )



def analyze_savings_scenarios(
    upfront_cost: float,
    conservative_annual_gross_savings: float,
    expected_annual_gross_savings: float,
    optimistic_annual_gross_savings: float,
    annual_maintenance_cost: float,
) -> dict[str, dict[str, float | None]]:
    """Compare investment returns under three savings assumptions."""

    if upfront_cost <= 0:
        raise ValueError("Upfront cost must be greater than zero.")

    if annual_maintenance_cost < 0:
        raise ValueError("Maintenance cost cannot be negative.")

    savings_values = [
        conservative_annual_gross_savings,
        expected_annual_gross_savings,
        optimistic_annual_gross_savings,
    ]

    if any(value < 0 for value in savings_values):
        raise ValueError("Annual savings cannot be negative.")

    if not (
        conservative_annual_gross_savings
        <= expected_annual_gross_savings
        <= optimistic_annual_gross_savings
    ):
        raise ValueError(
            "Savings must follow this order: "
            "conservative <= expected <= optimistic."
        )

    scenarios = {
        "conservative": conservative_annual_gross_savings,
        "expected": expected_annual_gross_savings,
        "optimistic": optimistic_annual_gross_savings,
    }

    results = {}

    for scenario_name, annual_savings in scenarios.items():
        investment_result = estimate_investment_return(
            upfront_cost=upfront_cost,
            expected_annual_gross_savings=annual_savings,
            annual_maintenance_cost=annual_maintenance_cost,
        )

        results[scenario_name] = {
            "annual_gross_savings": annual_savings,
            **investment_result,
        }

    return results


def summarize_investments(
    investments: list[dict[str, str | float | bool | None]],
    available_budget: float | None = None,
) -> dict[str, str | None]:
    """Summarize investment options using three transparent criteria."""

    if not investments:
        raise ValueError("At least one investment option is required.")

    if available_budget is not None and available_budget < 0:
        raise ValueError("Available budget cannot be negative.")

    eligible = [
        investment
        for investment in investments
        if (
            available_budget is None
            or investment.get("within_budget") is True
        )
    ]

    if not eligible:
        return {
            "status": "No investments fit the available budget.",
            "highest_annual_benefit": None,
            "highest_first_year_roi": None,
            "fastest_payback": None,
        }

    highest_benefit = max(
        eligible,
        key=lambda item: float(item["annual_net_benefit"]),
    )

    highest_roi = max(
        eligible,
        key=lambda item: float(item["first_year_roi_percent"]),
    )

    investments_with_payback = [
        item
        for item in eligible
        if item["payback_months"] is not None
    ]

    fastest_payback = (
        min(
            investments_with_payback,
            key=lambda item: float(item["payback_months"]),
        )
        if investments_with_payback
        else None
    )

    return {
        "status": "Comparison completed.",
        "highest_annual_benefit": str(highest_benefit["name"]),
        "highest_first_year_roi": str(highest_roi["name"]),
        "fastest_payback": (
            str(fastest_payback["name"])
            if fastest_payback is not None
            else None
        ),
    }



def estimate_preventable_impact(
    observed_impact_eur: float,
    preventable_fraction: float,
    observation_days: int,
) -> dict[str, float]:
    """Estimate potentially prevented impact and annualized gross savings."""

    values = {
        "Observed impact": observed_impact_eur,
        "Preventable fraction": preventable_fraction,
        "Observation days": observation_days,
    }

    for label, value in values.items():
        if not math.isfinite(value):
            raise ValueError(f"{label} must be a finite number.")

    if observed_impact_eur < 0:
        raise ValueError("Observed impact cannot be negative.")

    if not 0 <= preventable_fraction <= 1:
        raise ValueError("Preventable fraction must be between 0 and 1.")

    if observation_days <= 0:
        raise ValueError("Observation days must be greater than zero.")

    estimated_preventable_impact = (
        observed_impact_eur * preventable_fraction
    )

    estimated_annual_gross_savings = (
        estimated_preventable_impact * 365 / observation_days
    )

    return {
        "observed_impact_eur": observed_impact_eur,
        "estimated_preventable_impact_eur": estimated_preventable_impact,
        "estimated_annual_gross_savings_eur": estimated_annual_gross_savings,
    }

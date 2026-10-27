
import pytest

from src.business_calculations import (
    analyze_savings_scenarios,
    compare_investments,
    estimate_annual_impact,
    estimate_investment_return,
    summarize_investments,
    estimate_preventable_impact,
)


def test_estimate_annual_impact_returns_expected_values():
    result = estimate_annual_impact(
        outages_per_year=4,
        average_duration_hours=1.5,
        affected_transactions_per_hour=80,
        contribution_per_transaction=4,
        lost_transaction_fraction=0.60,
        recovery_cost_per_outage=75,
    )

    assert result["estimated_lost_transactions"] == 288
    assert result["lost_contribution"] == 1152
    assert result["annual_recovery_cost"] == 300
    assert result["total_annual_impact"] == 1452


def test_invalid_lost_transaction_fraction_is_rejected():
    with pytest.raises(ValueError):
        estimate_annual_impact(
            outages_per_year=4,
            average_duration_hours=1.5,
            affected_transactions_per_hour=80,
            contribution_per_transaction=4,
            lost_transaction_fraction=1.5,
            recovery_cost_per_outage=75,
        )


def test_profitable_investment_returns_expected_values():
    result = estimate_investment_return(
        upfront_cost=400,
        expected_annual_gross_savings=726,
        annual_maintenance_cost=200,
    )

    assert result["annual_net_benefit"] == 526
    assert result["payback_months"] == pytest.approx(9.125475)
    assert result["first_year_roi_percent"] == pytest.approx(31.5)


def test_investment_without_positive_benefit_has_no_payback_period():
    result = estimate_investment_return(
        upfront_cost=1000,
        expected_annual_gross_savings=400,
        annual_maintenance_cost=500,
    )

    assert result["annual_net_benefit"] == -100
    assert result["payback_months"] is None
    assert result["first_year_roi_percent"] == pytest.approx(-110)


def test_zero_upfront_cost_is_rejected():
    with pytest.raises(ValueError):
        estimate_investment_return(
            upfront_cost=0,
            expected_annual_gross_savings=726,
            annual_maintenance_cost=200,
        )


def test_compare_investments_ranks_options_by_annual_net_benefit():
    investments = [
        {
            "name": "Backup internet",
            "upfront_cost": 400,
            "expected_annual_gross_savings": 726,
            "annual_maintenance_cost": 200,
        },
        {
            "name": "Wi-Fi equipment upgrade",
            "upfront_cost": 1200,
            "expected_annual_gross_savings": 1000,
            "annual_maintenance_cost": 300,
        },
        {
            "name": "IT support contract",
            "upfront_cost": 100,
            "expected_annual_gross_savings": 350,
            "annual_maintenance_cost": 100,
        },
    ]

    results = compare_investments(investments)

    assert [option["name"] for option in results] == [
        "Wi-Fi equipment upgrade",
        "Backup internet",
        "IT support contract",
    ]

    assert results[0]["annual_net_benefit"] == 700
    assert results[1]["annual_net_benefit"] == 526
    assert results[2]["annual_net_benefit"] == 250


def test_compare_investments_rejects_empty_list():
    with pytest.raises(ValueError, match="At least one investment"):
        compare_investments([])


def test_compare_investments_rejects_missing_information():
    investments = [
        {
            "name": "Backup internet",
            "upfront_cost": 400,
            "expected_annual_gross_savings": 726,
        }
    ]

    with pytest.raises(ValueError, match="annual_maintenance_cost"):
        compare_investments(investments)


def test_savings_scenarios_calculate_expected_results():
    results = analyze_savings_scenarios(
        upfront_cost=400,
        conservative_annual_gross_savings=500,
        expected_annual_gross_savings=726,
        optimistic_annual_gross_savings=900,
        annual_maintenance_cost=200,
    )

    assert results["conservative"]["annual_net_benefit"] == 300
    assert results["expected"]["annual_net_benefit"] == 526
    assert results["optimistic"]["annual_net_benefit"] == 700

    assert results["conservative"]["payback_months"] == pytest.approx(16)
    assert results["expected"]["payback_months"] == pytest.approx(9.125475)
    assert results["optimistic"]["payback_months"] == pytest.approx(400 / 700 * 12)


def test_savings_scenarios_reject_wrong_order():
    with pytest.raises(ValueError, match="conservative <= expected <= optimistic"):
        analyze_savings_scenarios(
            upfront_cost=400,
            conservative_annual_gross_savings=800,
            expected_annual_gross_savings=600,
            optimistic_annual_gross_savings=900,
            annual_maintenance_cost=200,
        )


def test_savings_scenarios_reject_negative_savings():
    with pytest.raises(ValueError, match="Annual savings cannot be negative"):
        analyze_savings_scenarios(
            upfront_cost=400,
            conservative_annual_gross_savings=-100,
            expected_annual_gross_savings=500,
            optimistic_annual_gross_savings=900,
            annual_maintenance_cost=200,
        )


def test_budget_comparison_prioritises_affordable_investments():
    investments = [
        {
            "name": "Backup internet",
            "upfront_cost": 400,
            "expected_annual_gross_savings": 726,
            "annual_maintenance_cost": 200,
        },
        {
            "name": "Wi-Fi upgrade",
            "upfront_cost": 1200,
            "expected_annual_gross_savings": 1000,
            "annual_maintenance_cost": 300,
        },
        {
            "name": "IT support contract",
            "upfront_cost": 100,
            "expected_annual_gross_savings": 350,
            "annual_maintenance_cost": 100,
        },
    ]

    results = compare_investments(
        investments,
        available_budget=500,
    )

    assert [item["name"] for item in results] == [
        "Backup internet",
        "IT support contract",
        "Wi-Fi upgrade",
    ]

    assert results[0]["within_budget"] is True
    assert results[1]["within_budget"] is True
    assert results[2]["within_budget"] is False


def test_budget_comparison_rejects_negative_budget():
    investments = [
        {
            "name": "Backup internet",
            "upfront_cost": 400,
            "expected_annual_gross_savings": 726,
            "annual_maintenance_cost": 200,
        }
    ]

    with pytest.raises(ValueError, match="Available budget cannot be negative"):
        compare_investments(
            investments,
            available_budget=-100,
        )


def test_summary_identifies_different_leaders():
    results = compare_investments(
        [
            {
                "name": "Backup internet",
                "upfront_cost": 400,
                "expected_annual_gross_savings": 726,
                "annual_maintenance_cost": 200,
            },
            {
                "name": "Wi-Fi upgrade",
                "upfront_cost": 1200,
                "expected_annual_gross_savings": 1000,
                "annual_maintenance_cost": 300,
            },
            {
                "name": "IT support contract",
                "upfront_cost": 100,
                "expected_annual_gross_savings": 350,
                "annual_maintenance_cost": 100,
            },
        ]
    )

    summary = summarize_investments(results)

    assert summary["highest_annual_benefit"] == "Wi-Fi upgrade"
    assert summary["highest_first_year_roi"] == "IT support contract"
    assert summary["fastest_payback"] == "IT support contract"


def test_summary_reports_when_no_option_fits_budget():
    results = compare_investments(
        [
            {
                "name": "Wi-Fi upgrade",
                "upfront_cost": 1200,
                "expected_annual_gross_savings": 1000,
                "annual_maintenance_cost": 300,
            },
        ],
        available_budget=500,
    )

    summary = summarize_investments(
        results,
        available_budget=500,
    )

    assert summary["status"] == "No investments fit the available budget."
    assert summary["highest_annual_benefit"] is None
    assert summary["highest_first_year_roi"] is None
    assert summary["fastest_payback"] is None


def test_estimate_preventable_impact_calculates_savings():
    result = estimate_preventable_impact(
        observed_impact_eur=1000,
        preventable_fraction=0.5,
        observation_days=50,
    )

    assert result["observed_impact_eur"] == 1000
    assert result["estimated_preventable_impact_eur"] == pytest.approx(500)
    assert result["estimated_annual_gross_savings_eur"] == pytest.approx(3650)


def test_estimate_preventable_impact_rejects_negative_impact():
    with pytest.raises(ValueError):
        estimate_preventable_impact(-100, 0.5, 50)


def test_estimate_preventable_impact_rejects_fraction_below_zero():
    with pytest.raises(ValueError):
        estimate_preventable_impact(1000, -0.1, 50)


def test_estimate_preventable_impact_rejects_fraction_above_one():
    with pytest.raises(ValueError):
        estimate_preventable_impact(1000, 1.1, 50)


def test_estimate_preventable_impact_rejects_zero_observation_days():
    with pytest.raises(ValueError):
        estimate_preventable_impact(1000, 0.5, 0)


def test_investment_rejects_nan_savings():
    with pytest.raises(ValueError):
        estimate_investment_return(
            upfront_cost=400,
            expected_annual_gross_savings=float("nan"),
            annual_maintenance_cost=200,
        )


def test_investment_rejects_infinite_upfront_cost():
    with pytest.raises(ValueError):
        estimate_investment_return(
            upfront_cost=float("inf"),
            expected_annual_gross_savings=726,
            annual_maintenance_cost=200,
        )


def test_preventable_impact_rejects_nan_fraction():
    with pytest.raises(ValueError):
        estimate_preventable_impact(
            observed_impact_eur=1000,
            preventable_fraction=float("nan"),
            observation_days=50,
        )


def test_annual_impact_rejects_negative_outage_frequency():
    with pytest.raises(ValueError, match="Outages per year cannot be negative"):
        estimate_annual_impact(
            outages_per_year=-1,
            average_duration_hours=1.5,
            affected_transactions_per_hour=80,
            contribution_per_transaction=4,
            lost_transaction_fraction=0.5,
            recovery_cost_per_outage=75,
        )

def test_annual_impact_rejects_nan_duration():
    with pytest.raises(ValueError):
        estimate_annual_impact(
            outages_per_year=10,
            average_duration_hours=float("nan"),
            affected_transactions_per_hour=80,
            contribution_per_transaction=4,
            lost_transaction_fraction=0.5,
            recovery_cost_per_outage=75,
        )


def test_annual_impact_rejects_infinite_recovery_cost():
    with pytest.raises(ValueError):
        estimate_annual_impact(
            outages_per_year=10,
            average_duration_hours=1.5,
            affected_transactions_per_hour=80,
            contribution_per_transaction=4,
            lost_transaction_fraction=0.5,
            recovery_cost_per_outage=float("inf"),
        )


def test_savings_scenarios_reject_nan_savings():
    with pytest.raises(ValueError):
        analyze_savings_scenarios(
            upfront_cost=400,
            conservative_annual_gross_savings=500,
            expected_annual_gross_savings=float("nan"),
            optimistic_annual_gross_savings=900,
            annual_maintenance_cost=200,
        )


def test_savings_scenarios_reject_infinite_upfront_cost():
    with pytest.raises(ValueError):
        analyze_savings_scenarios(
            upfront_cost=float("inf"),
            conservative_annual_gross_savings=500,
            expected_annual_gross_savings=700,
            optimistic_annual_gross_savings=900,
            annual_maintenance_cost=200,
        )


def test_preventable_impact_rejects_infinite_observed_impact():
    with pytest.raises(ValueError):
        estimate_preventable_impact(
            observed_impact_eur=float("inf"),
            preventable_fraction=0.5,
            observation_days=50,
        )


def test_preventable_impact_rejects_infinite_observation_fraction():
    with pytest.raises(ValueError):
        estimate_preventable_impact(
            observed_impact_eur=1000,
            preventable_fraction=float("inf"),
            observation_days=50,
        )


def test_compare_investments_rejects_nan_budget():
    investments = [
        {
            "name": "Backup internet",
            "upfront_cost": 400,
            "expected_annual_gross_savings": 700,
            "annual_maintenance_cost": 200,
        }
    ]

    with pytest.raises(ValueError):
        compare_investments(
            investments,
            available_budget=float("nan"),
        )


def test_compare_investments_rejects_infinite_budget():
    investments = [
        {
            "name": "Backup internet",
            "upfront_cost": 400,
            "expected_annual_gross_savings": 700,
            "annual_maintenance_cost": 200,
        }
    ]

    with pytest.raises(ValueError):
        compare_investments(
            investments,
            available_budget=float("inf"),
        )

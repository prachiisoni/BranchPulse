
import pandas as pd

from src.incident_data import validate_incident_data


def make_valid_data():
    return pd.DataFrame(
        [
            {
                "incident_id": "INC-001",
                "incident_date": "2026-09-03",
                "branch": "Branch A",
                "incident_type": "Wi-Fi outage",
                "duration_hours": 1.5,
                "transactions_per_hour": 80,
                "contribution_per_transaction_eur": 4.0,
                "lost_transaction_fraction": 0.6,
                "recovery_cost_eur": 75,
            },
            {
                "incident_id": "INC-002",
                "incident_date": "2026-09-08",
                "branch": "Branch B",
                "incident_type": "Internet outage",
                "duration_hours": 2.0,
                "transactions_per_hour": 65,
                "contribution_per_transaction_eur": 5.0,
                "lost_transaction_fraction": 0.7,
                "recovery_cost_eur": 100,
            },
        ]
    )


def test_valid_incident_data_has_no_errors():
    assert validate_incident_data(make_valid_data()) == []


def test_missing_required_column_is_detected():
    data = make_valid_data().drop(columns=["branch"])

    errors = validate_incident_data(data)

    assert any("Missing required columns: branch" in error for error in errors)


def test_duplicate_incident_ids_are_detected():
    data = make_valid_data()
    data.loc[1, "incident_id"] = "INC-001"

    errors = validate_incident_data(data)

    assert any("duplicate incident IDs" in error for error in errors)



def test_invalid_date_and_numeric_value_are_detected():
    data = make_valid_data()
    data.loc[0, "incident_date"] = "not-a-date"

    # Allow the column to contain text so we can test invalid input.
    data["duration_hours"] = data["duration_hours"].astype(object)
    data.loc[1, "duration_hours"] = "unknown"

    errors = validate_incident_data(data)

    assert any("invalid date" in error for error in errors)
    assert any("duration_hours" in error for error in errors)



def test_negative_cost_and_invalid_fraction_are_detected():
    data = make_valid_data()
    data.loc[0, "recovery_cost_eur"] = -50
    data.loc[1, "lost_transaction_fraction"] = 1.5

    errors = validate_incident_data(data)

    assert any("recovery_cost_eur" in error for error in errors)
    assert any("between 0 and 1" in error for error in errors)


def test_empty_dataset_is_detected():
    data = make_valid_data().iloc[0:0]

    errors = validate_incident_data(data)

    assert any("contains no records" in error for error in errors)


def test_blank_branch_is_detected():
    data = make_valid_data()
    data.loc[0, "branch"] = " "

    errors = validate_incident_data(data)

    assert any("branch" in error and "blank value" in error for error in errors)

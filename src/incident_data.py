
import pandas as pd


REQUIRED_COLUMNS = [
    "incident_id",
    "incident_date",
    "branch",
    "incident_type",
    "duration_hours",
    "transactions_per_hour",
    "contribution_per_transaction_eur",
    "lost_transaction_fraction",
    "recovery_cost_eur",
]

NON_NEGATIVE_COLUMNS = [
    "duration_hours",
    "transactions_per_hour",
    "contribution_per_transaction_eur",
    "recovery_cost_eur",
]


def validate_incident_data(data: pd.DataFrame) -> list[str]:
    """Return a list of data-quality problems found in incident records."""

    errors = []

    if data.empty:
        errors.append("The incident dataset contains no records.")

    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(data.columns))

    if missing_columns:
        errors.append(
            "Missing required columns: " + ", ".join(missing_columns) + "."
        )
        return errors

    if data.empty:
        return errors

    # Incident IDs must be present and unique.
    incident_ids = data["incident_id"].astype("string").str.strip()

    blank_ids = (
        incident_ids.isna() | incident_ids.eq("")
    ).fillna(True)

    if blank_ids.any():
        errors.append(
            f"{int(blank_ids.sum())} row(s) have a missing incident ID."
        )

    valid_ids = incident_ids[~blank_ids]
    duplicate_rows = valid_ids.duplicated(keep=False)

    if duplicate_rows.any():
        errors.append(
            f"{int(duplicate_rows.sum())} row(s) have duplicate incident IDs."
        )

    # Dates must be valid.
    dates = pd.to_datetime(
        data["incident_date"],
        format="%Y-%m-%d",
        errors="coerce",
    )

    invalid_dates = dates.isna()

    if invalid_dates.any():
        errors.append(
            f"{int(invalid_dates.sum())} row(s) have a missing or invalid date."
        )

    # Branch and incident type must be populated.
    for column in ["branch", "incident_type"]:
        values = data[column].astype("string").str.strip()
        missing_values = (
            values.isna() | values.eq("")
        ).fillna(True)

        if missing_values.any():
            errors.append(
                f"Column '{column}' contains "
                f"{int(missing_values.sum())} blank value(s)."
            )

    # Numeric inputs must be valid numbers and non-negative.
    numeric_columns = (
        NON_NEGATIVE_COLUMNS + ["lost_transaction_fraction"]
    )

    numeric_values = {}

    for column in numeric_columns:
        values = pd.to_numeric(data[column], errors="coerce")
        numeric_values[column] = values

        invalid_values = values.isna()

        if invalid_values.any():
            errors.append(
                f"Column '{column}' contains "
                f"{int(invalid_values.sum())} missing or non-numeric value(s)."
            )

    for column in NON_NEGATIVE_COLUMNS:
        negative_values = numeric_values[column] < 0

        if negative_values.fillna(False).any():
            errors.append(
                f"Column '{column}' cannot contain negative values."
            )

    # A lost-transaction fraction must be between 0 and 1.
    lost_fraction = numeric_values["lost_transaction_fraction"]

    invalid_fractions = (
        (lost_fraction < 0) | (lost_fraction > 1)
    ).fillna(False)

    if invalid_fractions.any():
        errors.append(
            "Column 'lost_transaction_fraction' must contain values "
            "between 0 and 1."
        )

    return errors

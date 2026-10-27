from src.business_calculations import (
    analyze_savings_scenarios,
    compare_investments,
    estimate_annual_impact,
    estimate_investment_return,
)

def read_number(
    prompt: str,
    minimum: float = 0,
    maximum: float | None = None,
    allow_zero: bool = True,
) -> float:
    """Ask the user for a number and validate the input."""

    while True:
        raw_value = input(prompt).strip()

        try:
            value = float(raw_value)
        except ValueError:
            print("Please enter a valid number, such as 4 or 1.5.")
            continue

        if value < minimum or (not allow_zero and value == 0):
            print(f"Please enter a number greater than {minimum}.")

            if minimum == 0 and not allow_zero:
                print("Zero is not allowed for this value.")

            continue

        if maximum is not None and value > maximum:
            print(f"Please enter a number no greater than {maximum}.")
            continue

        return value


def read_non_negative_integer(prompt: str) -> int:
    """Ask for a whole number that is zero or greater."""

    while True:
        raw_value = input(prompt).strip()

        try:
            value = int(raw_value)
        except ValueError:
            print("Please enter a whole number, such as 0 or 4.")
            continue

        if value < 0:
            print("Please enter zero or a positive number.")
            continue

        return value


def show_impact_calculator() -> None:
    """Collect incident assumptions and estimate annual impact."""

    print("\n--- Annual Business Impact ---")
    print("Enter the business's estimated annual outage information.")

    outages = read_non_negative_integer("Outages per year: ")

    duration = read_number("Average outage duration (hours): ")

    transactions = read_number(
        "Transactions affected per hour: "
    )

    contribution = read_number(
        "Contribution per transaction (€): "
    )

    lost_fraction = read_number(
        "Fraction of affected transactions genuinely lost (0 to 1): ",
        maximum=1,
    )

    recovery_cost = read_number(
        "Recovery cost per outage (€): "
    )

    result = estimate_annual_impact(
        outages_per_year=outages,
        average_duration_hours=duration,
        affected_transactions_per_hour=transactions,
        contribution_per_transaction=contribution,
        lost_transaction_fraction=lost_fraction,
        recovery_cost_per_outage=recovery_cost,
    )

    print("\n--- Estimated Annual Impact ---")
    print(
        "Estimated lost transactions: "
        f"{result['estimated_lost_transactions']:,.1f}"
    )
    print(
        "Lost contribution: "
        f"€{result['lost_contribution']:,.2f}"
    )
    print(
        "Recovery costs: "
        f"€{result['annual_recovery_cost']:,.2f}"
    )
    print(
        "Total estimated annual impact: "
        f"€{result['total_annual_impact']:,.2f}"
    )

    print("\nThese are estimates based on the assumptions you entered.")


def show_investment_calculator() -> None:
    """Collect investment information and estimate financial returns."""

    print("\n--- Technology Investment Comparison ---")

    upfront_cost = read_number(
        "One-time implementation cost (€): ",
        allow_zero=False,
    )

    gross_savings = read_number(
        "Expected gross savings per year (€): "
    )

    maintenance = read_number(
        "Expected maintenance cost per year (€): "
    )

    result = estimate_investment_return(
        upfront_cost=upfront_cost,
        expected_annual_gross_savings=gross_savings,
        annual_maintenance_cost=maintenance,
    )

    print("\n--- Estimated Investment Results ---")
    print(
        "Annual net benefit: "
        f"€{result['annual_net_benefit']:,.2f}"
    )

    if result["payback_months"] is None:
        print("Payback period: No payback under these assumptions.")
    else:
        print(
            "Simple payback period: "
            f"{result['payback_months']:.1f} months"
        )

    print(
        "First-year ROI: "
        f"{result['first_year_roi_percent']:.1f}%"
    )

    print("\nResults are estimates, not guaranteed savings or returns.")


def show_investment_comparison() -> None:
    """Collect several investment options and rank them."""

    print("\n--- Compare Technology Investments ---")

    while True:
        raw_count = input(
            "How many investments do you want to compare? (2-5): "
        ).strip()

        try:
            number_of_options = int(raw_count)
        except ValueError:
            print("Please enter a whole number between 2 and 5.")
            continue

        if 2 <= number_of_options <= 5:
            break

        print("Please enter a number between 2 and 5.")

    investments = []

    for index in range(number_of_options):
        print(f"\nInvestment {index + 1}")

        while True:
            name = input("Investment name: ").strip()

            if name:
                break

            print("The investment name cannot be empty.")

        upfront_cost = read_number(
            "One-time implementation cost (€): ",
            allow_zero=False,
        )

        gross_savings = read_number(
            "Expected gross savings per year (€): "
        )

        maintenance_cost = read_number(
            "Expected maintenance cost per year (€): "
        )

        investments.append({
            "name": name,
            "upfront_cost": upfront_cost,
            "expected_annual_gross_savings": gross_savings,
            "annual_maintenance_cost": maintenance_cost,
        })

    results = compare_investments(investments)

    print("\n=== Investment Comparison ===")
    print("Ranked by estimated annual net benefit")
    print("All amounts are estimates based on user inputs.\n")

    for rank, result in enumerate(results, start=1):
        print(f"{rank}. {result['name']}")
        print(
            "   Annual net benefit: "
            f"€{result['annual_net_benefit']:,.2f}"
        )

        payback = result["payback_months"]

        if payback is None:
            print("   Payback: No payback under these assumptions.")
        else:
            print(f"   Payback: {payback:.1f} months")

        print(
            "   First-year ROI: "
            f"{result['first_year_roi_percent']:.1f}%"
        )
        print()


def show_savings_sensitivity_analysis() -> None:
    """Compare an investment under three savings scenarios."""

    print("\n--- Savings Sensitivity Analysis ---")
    print("Enter conservative, expected and optimistic estimates.")

    upfront_cost = read_number(
        "One-time implementation cost (€): ",
        allow_zero=False,
    )

    maintenance_cost = read_number(
        "Annual maintenance cost (€): "
    )

    conservative_savings = read_number(
        "Conservative gross annual savings (€): "
    )

    expected_savings = read_number(
        "Expected gross annual savings (€): "
    )

    optimistic_savings = read_number(
        "Optimistic gross annual savings (€): "
    )

    try:
        results = analyze_savings_scenarios(
            upfront_cost=upfront_cost,
            conservative_annual_gross_savings=conservative_savings,
            expected_annual_gross_savings=expected_savings,
            optimistic_annual_gross_savings=optimistic_savings,
            annual_maintenance_cost=maintenance_cost,
        )
    except ValueError as error:
        print(f"\nUnable to analyse scenarios: {error}")
        print(
            "Check that savings follow this order: "
            "conservative <= expected <= optimistic."
        )
        return

    print("\n=== Sensitivity Analysis Results ===")

    for scenario_name, result in results.items():
        print(f"\n{scenario_name.title()} scenario")
        print(
            "Gross annual savings: "
            f"€{result['annual_gross_savings']:,.2f}"
        )
        print(
            "Annual net benefit: "
            f"€{result['annual_net_benefit']:,.2f}"
        )

        payback = result["payback_months"]

        if payback is None:
            print("Payback: No payback under these assumptions.")
        else:
            print(f"Payback: {payback:.1f} months")

        print(
            "First-year ROI: "
            f"{result['first_year_roi_percent']:.1f}%"
        )

    print(
        "\nThese are hypothetical scenarios, "
        "not predictions or guaranteed savings."
    )


def main() -> None:
    """Display the BranchPulse menu."""

    while True:
        print("\n==============================")
        print("        BRANCHPULSE")
        print("==============================")
        print("1. Estimate annual business impact")
        print("2. Evaluate a technology investment")
        print("3. Compare multiple investments")
        print("4. Analyse savings scenarios")
        print("5. Exit")

        choice = input("\nChoose an option (1, 2, 3, 4 or 5): ").strip()

        if choice == "1":
            show_impact_calculator()
        elif choice == "2":
            show_investment_calculator()
        elif choice == "3":
            show_investment_comparison()
        elif choice == "4":
            show_savings_sensitivity_analysis()
        elif choice == "5":
            print("Thank you for using BranchPulse!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4 or 5.")

if __name__ == "__main__":
    main()

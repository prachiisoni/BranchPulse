
import pandas as pd
import plotly.express as px
import streamlit as st

from src.business_calculations import (
    analyze_savings_scenarios,
    compare_investments,
    estimate_annual_impact,
    estimate_investment_return,
    estimate_preventable_impact,
    summarize_investments,
)

from src.incident_data import validate_incident_data

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="BranchPulse",
    page_icon="📊",
    layout="wide",
)

st.title("BranchPulse")
st.subheader("Turn technology reliability into business decisions")

st.write(
    "Estimate the business impact of technology incidents, "
    "compare potential investments, and understand financial uncertainty."
)

st.info(
    "BranchPulse is an early-stage prototype. Results are estimates "
    "based on user-provided assumptions, not guaranteed savings."
)

impact_tab, single_tab, compare_tab, sensitivity_tab, incidents_tab, investment_tab = st.tabs(
    [
        "Business Impact",
        "Single Investment",
        "Compare Investments",
        "Sensitivity Analysis",
        "Incident Explorer",
        "Investment Planner",
    ]
)


# --------------------------------------------------
# TAB 1: ANNUAL BUSINESS IMPACT
# --------------------------------------------------

with impact_tab:
    st.header("Estimate Annual Business Impact")

    st.write(
        "Estimate lost contribution and direct recovery costs "
        "caused by technology outages."
    )

    with st.form("impact_form"):
        outages = st.number_input(
            "Outages per year",
            min_value=0,
            value=4,
            step=1,
        )

        duration = st.number_input(
            "Average outage duration (hours)",
            min_value=0.0,
            value=1.5,
            step=0.5,
        )

        transactions = st.number_input(
            "Transactions affected per hour",
            min_value=0.0,
            value=80.0,
            step=10.0,
        )

        contribution = st.number_input(
            "Contribution per transaction (€)",
            min_value=0.0,
            value=4.0,
            step=0.5,
        )

        lost_fraction = st.number_input(
            "Fraction of affected transactions genuinely lost",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.05,
            help="0.6 means 60% of affected transactions are genuinely lost.",
        )

        recovery_cost = st.number_input(
            "Recovery cost per outage (€)",
            min_value=0.0,
            value=75.0,
            step=25.0,
        )

        calculate_impact = st.form_submit_button(
            "Calculate Annual Impact"
        )

    if calculate_impact:
        result = estimate_annual_impact(
            outages_per_year=int(outages),
            average_duration_hours=duration,
            affected_transactions_per_hour=transactions,
            contribution_per_transaction=contribution,
            lost_transaction_fraction=lost_fraction,
            recovery_cost_per_outage=recovery_cost,
        )

        st.divider()
        st.subheader("Estimated Annual Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Lost contribution",
            f"€{result['lost_contribution']:,.2f}",
        )

        col2.metric(
            "Recovery costs",
            f"€{result['annual_recovery_cost']:,.2f}",
        )

        col3.metric(
            "Total annual impact",
            f"€{result['total_annual_impact']:,.2f}",
        )

        impact_data = pd.DataFrame(
            {
                "Component": [
                    "Lost contribution",
                    "Recovery costs",
                ],
                "Estimated amount (€)": [
                    result["lost_contribution"],
                    result["annual_recovery_cost"],
                ],
            }
        )

        figure = px.bar(
            impact_data,
            x="Component",
            y="Estimated amount (€)",
            title="Estimated Impact by Component",
        )

        st.plotly_chart(figure, use_container_width=True)


# --------------------------------------------------
# TAB 2: SINGLE INVESTMENT
# --------------------------------------------------

with single_tab:
    st.header("Evaluate One Technology Investment")

    st.write(
        "Estimate the financial return of a proposed technology investment."
    )

    with st.form("single_investment_form"):
        upfront_cost = st.number_input(
            "One-time implementation cost (€)",
            min_value=0.01,
            value=400.0,
            step=100.0,
        )

        gross_savings = st.number_input(
            "Expected gross savings per year (€)",
            min_value=0.0,
            value=726.0,
            step=100.0,
        )

        maintenance = st.number_input(
            "Expected maintenance cost per year (€)",
            min_value=0.0,
            value=200.0,
            step=50.0,
        )

        calculate_investment = st.form_submit_button(
            "Evaluate Investment"
        )

    if calculate_investment:
        result = estimate_investment_return(
            upfront_cost=upfront_cost,
            expected_annual_gross_savings=gross_savings,
            annual_maintenance_cost=maintenance,
        )

        st.divider()
        st.subheader("Estimated Investment Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Annual net benefit",
            f"€{result['annual_net_benefit']:,.2f}",
        )

        if result["payback_months"] is None:
            payback_text = "No payback"
        else:
            payback_text = f"{result['payback_months']:.1f} months"

        col2.metric("Simple payback", payback_text)

        col3.metric(
            "First-year ROI",
            f"{result['first_year_roi_percent']:.1f}%",
        )

        st.caption(
            "ROI includes annual maintenance costs and the upfront "
            "investment. Results depend on your assumptions."
        )


# --------------------------------------------------
# TAB 3: COMPARE MULTIPLE INVESTMENTS
# --------------------------------------------------

with compare_tab:
    st.header("Compare Technology Investments")

    st.write(
        "Compare two to five investment options. You can optionally "
        "prioritise options that fit your available upfront budget."
    )

    with st.form("compare_investments_form"):
        number_of_options = st.slider(
            "Number of investments",
            min_value=2,
            max_value=5,
            value=3,
        )

        use_budget = st.checkbox(
            "Prioritise investments within my upfront budget",
            value=False,
        )

        available_budget = None

        if use_budget:
            available_budget = st.number_input(
                "Available upfront budget (€)",
                min_value=0.0,
                value=500.0,
                step=100.0,
            )

        investments = []

        default_names = [
            "Backup internet",
            "Wi-Fi upgrade",
            "IT support contract",
            "Network monitoring",
            "Equipment replacement",
        ]

        default_costs = [400.0, 1200.0, 100.0, 500.0, 800.0]
        default_savings = [726.0, 1000.0, 350.0, 650.0, 900.0]
        default_maintenance = [200.0, 300.0, 100.0, 150.0, 200.0]

        for index in range(number_of_options):
            st.markdown(f"**Investment {index + 1}**")

            name = st.text_input(
                "Investment name",
                value=default_names[index],
                key=f"investment_name_{index}",
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                cost = st.number_input(
                    "Upfront cost (€)",
                    min_value=0.01,
                    value=default_costs[index],
                    step=100.0,
                    key=f"investment_cost_{index}",
                )

            with col2:
                savings = st.number_input(
                    "Gross annual savings (€)",
                    min_value=0.0,
                    value=default_savings[index],
                    step=100.0,
                    key=f"investment_savings_{index}",
                )

            with col3:
                maintenance_cost = st.number_input(
                    "Annual maintenance (€)",
                    min_value=0.0,
                    value=default_maintenance[index],
                    step=50.0,
                    key=f"investment_maintenance_{index}",
                )

            investments.append(
                {
                    "name": name,
                    "upfront_cost": cost,
                    "expected_annual_gross_savings": savings,
                    "annual_maintenance_cost": maintenance_cost,
                }
            )

            st.divider()

        compare_button = st.form_submit_button(
            "Compare Investments"
        )

    if compare_button:
        if any(not item["name"].strip() for item in investments):
            st.error("Please provide a name for every investment.")

        else:
            results = compare_investments(
                investments,
                available_budget=available_budget,
            )

            st.subheader("Ranked Investment Results")

            display_data = pd.DataFrame(results)[
                [
                    "name",
                    "within_budget",
                    "annual_net_benefit",
                    "payback_months",
                    "first_year_roi_percent",
                ]
            ].rename(
                columns={
                    "name": "Investment",
                    "within_budget": "Budget status",
                    "annual_net_benefit": "Annual net benefit (€)",
                    "payback_months": "Payback (months)",
                    "first_year_roi_percent": "First-year ROI (%)",
                }
            )

            display_data["Budget status"] = display_data[
                "Budget status"
            ].map(
                lambda status: (
                    "Not assessed"
                    if pd.isna(status)
                    else "Within budget"
                    if status
                    else "Over budget"
                )
            )

            display_data["Payback (months)"] = display_data[
                "Payback (months)"
            ].map(
                lambda value: (
                    "No payback"
                    if pd.isna(value)
                    else f"{value:.1f}"
                )
            )

            st.dataframe(
                display_data,
                hide_index=True,
                use_container_width=True,
            )

            figure = px.bar(
                pd.DataFrame(results),
                x="name",
                y="annual_net_benefit",
                title="Annual Net Benefit by Investment",
                labels={
                    "name": "Investment",
                    "annual_net_benefit": "Annual net benefit (€)",
                },
            )

            st.plotly_chart(figure, use_container_width=True)

            # NEW: DECISION SUMMARY
            st.divider()
            st.subheader("Decision Summary")

            summary = summarize_investments(
                results,
                available_budget=available_budget,
            )

            if summary["status"] == "No investments fit the available budget.":
                st.warning(
                    "None of the investments fits your upfront budget. "
                    "Consider increasing the budget or evaluating a "
                    "lower-cost alternative."
                )

            else:
                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Highest annual net benefit",
                    summary["highest_annual_benefit"] or "N/A",
                )

                col2.metric(
                    "Highest first-year ROI",
                    summary["highest_first_year_roi"] or "N/A",
                )

                col3.metric(
                    "Fastest payback",
                    summary["fastest_payback"] or "No positive payback",
                )

                st.caption(
                    "These are three separate comparison criteria. "
                    "The leading option may differ for each criterion; "
                    "none is automatically the best overall choice."
                )

            if available_budget is None:
                st.caption(
                    "Options are ranked by annual net benefit. "
                    "No upfront budget was applied."
                )
            else:
                st.caption(
                    "Within-budget options appear first, ranked by annual "
                    "net benefit. Over-budget options remain visible. "
                    "This comparison does not assess ongoing affordability "
                    "or uncertainty."
                )


# --------------------------------------------------
# TAB 4: SAVINGS SENSITIVITY ANALYSIS
# --------------------------------------------------

with sensitivity_tab:
    st.header("Savings Sensitivity Analysis")

    st.write(
        "Explore how investment returns change when actual savings "
        "are lower or higher than your central estimate."
    )

    with st.form("sensitivity_form"):
        scenario_cost = st.number_input(
            "One-time implementation cost (€)",
            min_value=0.01,
            value=400.0,
            step=100.0,
        )

        scenario_maintenance = st.number_input(
            "Annual maintenance cost (€)",
            min_value=0.0,
            value=200.0,
            step=50.0,
        )

        conservative = st.number_input(
            "Conservative gross annual savings (€)",
            min_value=0.0,
            value=500.0,
            step=50.0,
        )

        expected = st.number_input(
            "Expected gross annual savings (€)",
            min_value=0.0,
            value=726.0,
            step=50.0,
        )

        optimistic = st.number_input(
            "Optimistic gross annual savings (€)",
            min_value=0.0,
            value=900.0,
            step=50.0,
        )

        run_sensitivity = st.form_submit_button(
            "Analyse Scenarios"
        )

    if run_sensitivity:
        try:
            results = analyze_savings_scenarios(
                upfront_cost=scenario_cost,
                conservative_annual_gross_savings=conservative,
                expected_annual_gross_savings=expected,
                optimistic_annual_gross_savings=optimistic,
                annual_maintenance_cost=scenario_maintenance,
            )

        except ValueError as error:
            st.error(str(error))

        else:
            st.subheader("Scenario Results")

            scenario_rows = []

            for scenario_name, result in results.items():
                scenario_rows.append(
                    {
                        "Scenario": scenario_name.title(),
                        "Gross annual savings (€)": (
                            result["annual_gross_savings"]
                        ),
                        "Annual net benefit (€)": (
                            result["annual_net_benefit"]
                        ),
                        "Payback (months)": (
                            result["payback_months"]
                        ),
                        "First-year ROI (%)": (
                            result["first_year_roi_percent"]
                        ),
                    }
                )

            scenario_data = pd.DataFrame(scenario_rows)

            scenario_data["Payback (months)"] = scenario_data[
                "Payback (months)"
            ].map(
                lambda value: (
                    "No payback"
                    if pd.isna(value)
                    else f"{value:.1f}"
                )
            )

            st.dataframe(
                scenario_data,
                hide_index=True,
                use_container_width=True,
            )

            figure = px.bar(
                scenario_data,
                x="Scenario",
                y="Annual net benefit (€)",
                title="How Savings Assumptions Affect Annual Benefit",
            )

            st.plotly_chart(figure, use_container_width=True)

            st.caption(
                "These are hypothetical scenarios, not probabilities "
                "or predictions of actual savings."
            )


with incidents_tab:
    st.header("Incident Explorer")
    st.write(
        "Review technology incidents across branches and estimate "
        "their potential financial impact."
    )

    try:
        incident_data = pd.read_csv(
            "data/sample_incidents.csv",
            parse_dates=["incident_date"],
        )
    except FileNotFoundError:
        st.error(
            "The incident dataset was not found. "
            "Check that data/sample_incidents.csv exists."
        )
    else:
        data_errors = validate_incident_data(incident_data)

        if data_errors:
            st.error(
                "Incident data failed validation. "
                "Financial calculations have been stopped."
            )

            for error in data_errors:
                st.write(f"- {error}")

            st.stop()
        incident_data["estimated_impact_eur"] = (
            incident_data["duration_hours"]
            * incident_data["transactions_per_hour"]
            * incident_data["contribution_per_transaction_eur"]
            * incident_data["lost_transaction_fraction"]
            + incident_data["recovery_cost_eur"]
        )

        st.subheader("Filter incidents")

        available_branches = sorted(
            incident_data["branch"].dropna().unique().tolist()
        )
        selected_branches = st.multiselect(
            "Branches",
            options=available_branches,
            default=available_branches,
            key="incident_explorer_branches",
        )

        available_types = sorted(
            incident_data["incident_type"].dropna().unique().tolist()
        )
        selected_types = st.multiselect(
            "Incident types",
            options=available_types,
            default=available_types,
            key="incident_explorer_types",
        )

        # Clearing a filter means include all values for that filter.
        branches_to_show = selected_branches or available_branches
        types_to_show = selected_types or available_types

        incident_data = incident_data[
            incident_data["branch"].isin(branches_to_show)
            & incident_data["incident_type"].isin(types_to_show)
        ].copy()

        if incident_data.empty:
            st.warning("No incidents match the selected filters. Try changing the branch or incident type.")
            st.stop()


        st.subheader("Filter by date")

        min_date = incident_data["incident_date"].min().date()
        max_date = incident_data["incident_date"].max().date()

        selected_dates = st.date_input(
            "Incident date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="incident_explorer_date_range",
        )

        if isinstance(selected_dates, (tuple, list)):
            if len(selected_dates) == 2:
                start_date, end_date = selected_dates

                incident_data = incident_data[
                    incident_data["incident_date"].dt.date.between(
                        start_date, end_date
                    )
                ].copy()
            elif len(selected_dates) == 1:
                st.info("Select an end date to complete the date range.")

        if incident_data.empty:
            st.warning(
                "No incidents occurred within the selected date range. "
                "Try selecting a different period."
            )
            st.stop()

        total_impact = incident_data["estimated_impact_eur"].sum()
        incident_count = len(incident_data)

        branch_impact = (
            incident_data.groupby("branch", as_index=False)[
                "estimated_impact_eur"
            ]
            .sum()
            .sort_values("estimated_impact_eur", ascending=False)
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Incidents", incident_count)
        col2.metric("Total estimated impact", f"€{total_impact:,.2f}")
        col3.metric(
            "Highest-impact branch",
            branch_impact.iloc[0]["branch"],
        )

        st.caption(
            "Estimates depend on assumed lost transactions and recovery costs. "
            "The displayed total covers only the incidents in this dataset."
        )

        st.subheader("Estimated impact by branch")
        st.bar_chart(
            branch_impact.set_index("branch")["estimated_impact_eur"]
        )


        st.subheader("Incident frequency vs. estimated impact")

        branch_summary = (
            incident_data.groupby("branch")
            .agg(
                incident_count=("incident_id", "count"),
                estimated_impact_eur=("estimated_impact_eur", "sum"),
            )
            .reset_index()
            .sort_values("estimated_impact_eur", ascending=False)
        )

        st.bar_chart(
            branch_summary.set_index("branch")["incident_count"]
        )

        st.caption(
            "This chart shows the number of incidents per branch. "
            "Compare it with the financial-impact chart above."
        )

        st.dataframe(
            branch_summary.rename(
                columns={
                    "branch": "Branch",
                    "incident_count": "Incident count",
                    "estimated_impact_eur": "Estimated impact (€)",
                }
            ).assign(
                **{
                    "Estimated impact (€)": lambda table: table[
                        "Estimated impact (€)"
                    ].round(2)
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        type_impact = (
            incident_data.groupby("incident_type", as_index=False)[
                "estimated_impact_eur"
            ]
            .sum()
            .sort_values("estimated_impact_eur", ascending=False)
        )

        st.subheader("Estimated impact by incident type")
        st.bar_chart(
            type_impact.set_index("incident_type")["estimated_impact_eur"]
        )

        st.subheader("Incident records")


        st.subheader("Weekly incident trends")

        weekly_summary = (
            incident_data.set_index("incident_date")
            .resample("W-SUN")
            .agg(
                incident_count=("incident_id", "count"),
                estimated_impact_eur=("estimated_impact_eur", "sum"),
            )
            .reset_index()
            .rename(columns={"incident_date": "week_ending"})
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Incidents per week**")
            st.line_chart(
                weekly_summary.set_index("week_ending")["incident_count"]
            )

        with col2:
            st.write("**Estimated impact per week (€)**")
            st.line_chart(
                weekly_summary.set_index("week_ending")[
                    "estimated_impact_eur"
                ]
            )

        st.caption(
            "Weeks end on Sunday. Weeks without recorded incidents are "
            "shown as zero. Trends reflect only the currently filtered "
            "sample data and are not forecasts."
        )


        display_data = incident_data.rename(
            columns={
                "incident_id": "Incident ID",
                "incident_date": "Incident date",
                "branch": "Branch",
                "incident_type": "Incident type",
                "duration_hours": "Duration (hours)",
                "transactions_per_hour": "Transactions per hour",
                "contribution_per_transaction_eur": "Contribution per transaction (€)",
                "lost_transaction_fraction": "Assumed lost fraction",
                "recovery_cost_eur": "Recovery cost (€)",
                "estimated_impact_eur": "Estimated impact (€)",
            }
        )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True,
        )


with investment_tab:
    st.header("Investment Planner")
    st.write(
        "Estimate how much incident impact an improvement might prevent "
        "and evaluate whether the resulting savings could justify its cost."
    )

    st.info(
        "This is an illustrative decision-support model. "
        "The preventable fraction and investment costs are user assumptions, "
        "not verified results."
    )

    planner_data = pd.read_csv(
        "data/sample_incidents.csv",
        parse_dates=["incident_date"],
    )

    planner_data["estimated_impact_eur"] = (
        planner_data["duration_hours"]
        * planner_data["transactions_per_hour"]
        * planner_data["contribution_per_transaction_eur"]
        * planner_data["lost_transaction_fraction"]
        + planner_data["recovery_cost_eur"]
    )

    planner_min_date = planner_data["incident_date"].min().date()
    planner_max_date = planner_data["incident_date"].max().date()

    branches = ["All branches"] + sorted(
        planner_data["branch"].dropna().unique().tolist()
    )

    selected_branch = st.selectbox(
        "Branch to evaluate",
        options=branches,
        key="planner_branch",
    )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start date",
            value=planner_min_date,
            min_value=planner_min_date,
            max_value=planner_max_date,
            key="planner_start_date",
        )

    with col2:
        end_date = st.date_input(
            "End date",
            value=planner_max_date,
            min_value=planner_min_date,
            max_value=planner_max_date,
            key="planner_end_date",
        )

    if start_date > end_date:
        st.error("The start date cannot be later than the end date.")
    else:
        selected_data = planner_data[
            planner_data["incident_date"].dt.date.between(
                start_date, end_date
            )
        ].copy()

        if selected_branch != "All branches":
            selected_data = selected_data[
                selected_data["branch"] == selected_branch
            ].copy()

        if selected_data.empty:
            st.warning(
                "No incidents match the selected branch and date range. "
                "Choose a different branch or period."
            )
        else:
            observation_days = (end_date - start_date).days + 1

            observed_impact = float(
                selected_data["estimated_impact_eur"].sum()
            )

            st.subheader("1. Estimate preventable impact")

            st.metric(
                "Observed estimated impact",
                f"€{observed_impact:,.2f}",
            )

            st.caption(
                f"Based on {len(selected_data)} incidents across "
                f"{observation_days} calendar days."
            )

            preventable_percentage = st.slider(
                "Assumed fraction of impact preventable by the improvement",
                min_value=0,
                max_value=100,
                value=25,
                step=5,
                format="%d%%",
                key="planner_preventable_percentage",
            )

            preventable_fraction = preventable_percentage / 100

            savings_estimate = estimate_preventable_impact(
                observed_impact_eur=observed_impact,
                preventable_fraction=preventable_fraction,
                observation_days=observation_days,
            )

            st.metric(
                "Estimated preventable impact in selected period",
                f"€{savings_estimate['estimated_preventable_impact_eur']:,.2f}",
            )

            st.metric(
                "Annualized gross savings estimate",
                f"€{savings_estimate['estimated_annual_gross_savings_eur']:,.2f}",
            )

            st.caption(
                "Annualization assumes the observed rate continues throughout "
                "the year. A short or synthetic dataset can produce unreliable "
                "projections. The selected preventable fraction is a scenario "
                "assumption, not evidence that the improvement will achieve it."
            )

            st.divider()
            st.subheader("2. Evaluate a proposed investment")

            col1, col2 = st.columns(2)

            with col1:
                upfront_cost = st.number_input(
                    "Upfront investment cost (€)",
                    min_value=1.0,
                    value=5000.0,
                    step=500.0,
                    key="planner_upfront_cost",
                )

            with col2:
                annual_maintenance_cost = st.number_input(
                    "Annual maintenance cost (€)",
                    min_value=0.0,
                    value=500.0,
                    step=100.0,
                    key="planner_maintenance_cost",
                )

            investment_result = estimate_investment_return(
                upfront_cost=upfront_cost,
                expected_annual_gross_savings=(
                    savings_estimate[
                        "estimated_annual_gross_savings_eur"
                    ]
                ),
                annual_maintenance_cost=annual_maintenance_cost,
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Annual net benefit",
                f"€{investment_result['annual_net_benefit']:,.2f}",
            )

            payback = investment_result["payback_months"]
            col2.metric(
                "Estimated payback",
                f"{payback:.1f} months" if payback is not None else "No payback",
            )

            col3.metric(
                "First-year ROI",
                f"{investment_result['first_year_roi_percent']:.1f}%",
            )

            st.caption(
                "These outputs depend on the selected incident history and "
                "your assumptions about preventable impact, investment cost, "
                "and maintenance. They are not a guarantee of future returns."
            )

            st.divider()
            st.subheader("3. Compare savings scenarios")

            st.write(
                "Test how the investment performs if the improvement "
                "prevents a different fraction of the estimated impact."
            )

            col1, col2 = st.columns(2)

            with col1:
                conservative_percentage = st.slider(
                    "Conservative scenario (%)",
                    min_value=0,
                    max_value=100,
                    value=10,
                    step=5,
                    key="planner_conservative_percentage",
                )

            with col2:
                optimistic_percentage = st.slider(
                    "Optimistic scenario (%)",
                    min_value=0,
                    max_value=100,
                    value=40,
                    step=5,
                    key="planner_optimistic_percentage",
                )

            if not (
                conservative_percentage
                <= preventable_percentage
                <= optimistic_percentage
            ):
                st.warning(
                    "Keep the scenarios in order: conservative percentage "
                    "<= expected percentage <= optimistic percentage."
                )
            else:
                scenario_rows = []

                scenarios = [
                    ("Conservative", conservative_percentage),
                    ("Expected", preventable_percentage),
                    ("Optimistic", optimistic_percentage),
                ]

                for scenario_name, percentage in scenarios:
                    scenario_savings = estimate_preventable_impact(
                        observed_impact_eur=observed_impact,
                        preventable_fraction=percentage / 100,
                        observation_days=observation_days,
                    )

                    scenario_return = estimate_investment_return(
                        upfront_cost=upfront_cost,
                        expected_annual_gross_savings=(
                            scenario_savings[
                                "estimated_annual_gross_savings_eur"
                            ]
                        ),
                        annual_maintenance_cost=annual_maintenance_cost,
                    )

                    payback_months = scenario_return["payback_months"]

                    scenario_rows.append(
                        {
                            "Scenario": scenario_name,
                            "Preventable fraction": f"{percentage}%",
                            "Annual gross savings (€)": round(
                                scenario_savings[
                                    "estimated_annual_gross_savings_eur"
                                ],
                                2,
                            ),
                            "Annual net benefit (€)": round(
                                scenario_return["annual_net_benefit"],
                                2,
                            ),
                            "Payback (months)": (
                                round(payback_months, 1)
                                if payback_months is not None
                                else "No payback"
                            ),
                            "First-year ROI (%)": round(
                                scenario_return["first_year_roi_percent"],
                                1,
                            ),
                        }
                    )

                st.dataframe(
                    pd.DataFrame(scenario_rows),
                    use_container_width=True,
                    hide_index=True,
                )


                # Prepare a report containing the assumptions and results.
                report_data = pd.DataFrame(scenario_rows).copy()

                report_data.insert(0, "Selected branch", selected_branch)
                report_data.insert(1, "Start date", start_date.isoformat())
                report_data.insert(2, "End date", end_date.isoformat())

                report_data["Observed estimated impact (€)"] = round(
                    observed_impact, 2
                )
                report_data["Observation days"] = observation_days
                report_data["Expected preventable fraction (%)"] = (
                    preventable_percentage
                )
                report_data["Upfront investment cost (€)"] = upfront_cost
                report_data["Annual maintenance cost (€)"] = (
                    annual_maintenance_cost
                )

                report_csv = report_data.to_csv(index=False).encode("utf-8-sig")

                st.download_button(
                    label="Download investment scenario report (CSV)",
                    data=report_csv,
                    file_name="branchpulse_investment_report.csv",
                    mime="text/csv",
                    key="planner_download_report",
                )

                st.caption(
                    "These scenarios are hypothetical assumptions, not "
                    "measured probabilities or guaranteed savings. The "
                    "annualized estimates assume the observed incident rate "
                    "continues throughout the year."
                )

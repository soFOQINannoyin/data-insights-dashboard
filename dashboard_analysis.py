"""
Resource Allocation Optimization Simulator
------------------------------------------
This project uses Linear Programming to:
- Allocate workload between teams
- Minimize cost and resource usage
- Improve operational efficiency

This mirrors real people operations / workforce planning problems
at global companies like Revolut.
"""

import pandas as pd
import pulp


# -------------------------------------------------------------------
# LOAD WORKLOAD DATA
# -------------------------------------------------------------------
def load_data(path="../data/workload_data.csv"):
    return pd.read_csv(path)


# -------------------------------------------------------------------
# BUILD OPTIMIZATION MODEL
# -------------------------------------------------------------------
def build_optimization_model(df):

    # Define LP problem (Minimization)
    problem = pulp.LpProblem("Resource_Allocation", pulp.LpMinimize)

    # Decision variables:
    # Hours allocated to each team
    team_vars = {
        row["Team"]: pulp.LpVariable(row["Team"], lowBound=0)
        for _, row in df.iterrows()
    }

    # Objective function:
    # Minimize total weighted cost = cost_per_hour * hours
    problem += pulp.lpSum([
        row["Cost_per_Hour"] * team_vars[row["Team"]]
        for _, row in df.iterrows()
    ])

    # Constraint:
    # Sum of (productivity_per_hour * hours) for all teams
    # must meet total required workload.
    total_required = df["Required_Hours"].sum()

    problem += pulp.lpSum([
        row["Productivity"] * team_vars[row["Team"]]
        for _, row in df.iterrows()
    ]) >= total_required, "Workload_Requirement"

    return problem, team_vars


# -------------------------------------------------------------------
# SOLVE MODEL
# -------------------------------------------------------------------
def solve_model(problem, team_vars):
    problem.solve()

    results = {team: var.value() for team, var in team_vars.items()}

    total_cost = pulp.value(problem.objective)

    return results, total_cost


# -------------------------------------------------------------------
# MAIN SIMULATION PIPELINE
# -------------------------------------------------------------------
def main():
    df = load_data()
    problem, team_vars = build_optimization_model(df)
    results, total_cost = solve_model(problem, team_vars)

    print("\n=========== RESOURCE ALLOCATION OUTPUT ===========\n")
    print("Optimal Hours Allocation:")
    for team, hours in results.items():
        print(f"  {team:20}: {round(hours, 2)} hrs")

    print(f"\nTotal Operational Cost: {round(total_cost, 2)} units")
    print("\n===================================================\n")


if __name__ == "__main__":
    main()

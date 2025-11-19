
"""
Data Insights Dashboard Simulation
----------------------------------
Performs analytics on operational data using pandas.
Mimics KPI dashboards used in Ops / People teams.
"""

import pandas as pd


# ---- SAMPLE DATA ----
data = {
    "Person": ["A", "B", "C", "D", "E"],
    "Tasks_Completed": [12, 8, 10, 15, 9],
    "Hours_Spent": [20, 15, 18, 25, 17],
    "Category": ["Academic", "Finance", "Academic", "IT", "Finance"]
}

df = pd.DataFrame(data)

# ---- COMPUTE ANALYTICS ----
df["Efficiency"] = df["Tasks_Completed"] / df["Hours_Spent"]
category_counts = df["Category"].value_counts()
avg_hours = df["Hours_Spent"].mean()


def main():
    print("=== DATA INSIGHTS REPORT ===\n")
    print("Category Distribution:\n", category_counts)
    print("\nAverage Hours Spent:", avg_hours)
    print("\nEfficiency Table:\n", df)


if __name__ == "__main__":
    main()

"""
Financial Performance Dashboard - EDA & Charts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE = Path(__file__).parent.parent
DATA = BASE / "data"
CHARTS = Path(__file__).parent / "charts"
CHARTS.mkdir(exist_ok=True)
SUMMARIES = DATA / "summaries"
SUMMARIES.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (11, 6)

df = pd.read_csv(DATA / "financial_data.csv", parse_dates=["Date"])
monthly = pd.read_csv(DATA / "monthly_summary.csv")

print("=" * 60)
print("FINANCIAL PERFORMANCE – OVERVIEW")
print("=" * 60)
rev = df.loc[df["Type"] == "Revenue", "Actual"].sum()
exp = df.loc[df["Type"] == "Expense", "Actual"].sum()
profit = rev - exp
print(f"Total Revenue : ${rev:,.2f}")
print(f"Total Expenses: ${exp:,.2f}")
print(f"Net Profit    : ${profit:,.2f}")
print(f"Profit Margin : {profit/rev*100:.2f}%")
print(f"Records       : {len(df):,}")
print(f"Date range    : {df['Date'].min().date()} → {df['Date'].max().date()}")

# Yearly
print("\n--- Yearly P&L ---")
yearly = df.groupby(["Year", "Type"])["Actual"].sum().unstack(fill_value=0)
yearly["Profit"] = yearly.get("Revenue", 0) - yearly.get("Expense", 0)
print(yearly.round(0))

# Charts
# 1. Monthly Revenue vs Expenses
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(monthly["YearMonth"], monthly["Actual_Revenue"], marker="o", label="Revenue", color="#4e79a7")
ax.plot(monthly["YearMonth"], monthly["Actual_Expense"], marker="o", label="Expenses", color="#e15759")
ax.set_title("Monthly Revenue vs Expenses")
ax.set_ylabel("Amount ($)")
ax.legend()
ax.tick_params(axis="x", rotation=60)
plt.tight_layout()
plt.savefig(CHARTS / "01_monthly_revenue_expenses.png", dpi=150)
plt.close()

# 2. Monthly Profit
fig, ax = plt.subplots(figsize=(14, 5))
colors = ["#59a14f" if x >= 0 else "#e15759" for x in monthly["Actual_Profit"]]
ax.bar(monthly["YearMonth"], monthly["Actual_Profit"], color=colors)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("Monthly Net Profit")
ax.set_ylabel("Profit ($)")
ax.tick_params(axis="x", rotation=60)
plt.tight_layout()
plt.savefig(CHARTS / "02_monthly_profit.png", dpi=150)
plt.close()

# 3. Revenue by Category
rev_cat = df[df["Type"] == "Revenue"].groupby("Category")["Actual"].sum().sort_values()
fig, ax = plt.subplots()
rev_cat.plot(kind="barh", color="#4e79a7", ax=ax)
ax.set_title("Revenue by Category")
ax.set_xlabel("Revenue ($)")
plt.tight_layout()
plt.savefig(CHARTS / "03_revenue_by_category.png", dpi=150)
plt.close()

# 4. Expenses by Category
exp_cat = df[df["Type"] == "Expense"].groupby("Category")["Actual"].sum().sort_values()
fig, ax = plt.subplots()
exp_cat.plot(kind="barh", color="#e15759", ax=ax)
ax.set_title("Expenses by Category")
ax.set_xlabel("Expenses ($)")
plt.tight_layout()
plt.savefig(CHARTS / "04_expenses_by_category.png", dpi=150)
plt.close()

# 5. Expenses by Department
exp_dept = df[df["Type"] == "Expense"].groupby("Department")["Actual"].sum().sort_values()
fig, ax = plt.subplots()
exp_dept.plot(kind="barh", color="#f28e2b", ax=ax)
ax.set_title("Expenses by Department")
ax.set_xlabel("Expenses ($)")
plt.tight_layout()
plt.savefig(CHARTS / "05_expenses_by_department.png", dpi=150)
plt.close()

# 6. Budget vs Actual by Type
comp = df.groupby("Type").agg(Actual=("Actual", "sum"), Budget=("Budget", "sum"))
fig, ax = plt.subplots()
comp.plot(kind="bar", ax=ax, color=["#4e79a7", "#76b7b2"])
ax.set_title("Budget vs Actual (Revenue & Expenses)")
ax.set_ylabel("Amount ($)")
ax.tick_params(axis="x", rotation=0)
plt.tight_layout()
plt.savefig(CHARTS / "06_budget_vs_actual.png", dpi=150)
plt.close()

# 7. Profit Margin trend
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(monthly["YearMonth"], monthly["Profit_Margin_Pct"], marker="o", color="#59a14f")
ax.axhline(0, color="gray", linestyle="--")
ax.set_title("Monthly Profit Margin %")
ax.set_ylabel("Margin (%)")
ax.tick_params(axis="x", rotation=60)
plt.tight_layout()
plt.savefig(CHARTS / "07_profit_margin_trend.png", dpi=150)
plt.close()

# 8. Yearly comparison
fig, ax = plt.subplots()
yearly[["Revenue", "Expense", "Profit"]].plot(kind="bar", ax=ax, color=["#4e79a7", "#e15759", "#59a14f"])
ax.set_title("Yearly Revenue, Expenses & Profit")
ax.set_ylabel("Amount ($)")
ax.tick_params(axis="x", rotation=0)
plt.tight_layout()
plt.savefig(CHARTS / "08_yearly_comparison.png", dpi=150)
plt.close()

print(f"\nCharts saved to {CHARTS}")

# Exports
kpi = pd.DataFrame([{
    "Total_Revenue": round(rev, 2),
    "Total_Expenses": round(exp, 2),
    "Net_Profit": round(profit, 2),
    "Profit_Margin_Pct": round(profit / rev * 100, 2)
}])
kpi.to_csv(SUMMARIES / "overall_kpis.csv", index=False)
rev_cat.to_csv(SUMMARIES / "revenue_by_category.csv")
exp_cat.to_csv(SUMMARIES / "expenses_by_category.csv")
exp_dept.to_csv(SUMMARIES / "expenses_by_department.csv")
monthly.to_csv(SUMMARIES / "monthly_pnl.csv", index=False)
print(f"Summaries → {SUMMARIES}")
print("\n✅ Financial analysis complete.")

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

df = pd.read_csv("responses.csv")

print("First few rows:")
print(df.head())

print("\nSummary by load condition:")
summary = df.groupby("load").agg(
    total_trials=("choice", "count"),
    risky_choices=("choice", lambda x: (x == "Risky").sum()),
    risk_rate=("choice", lambda x: (x == "Risky").mean()),
    avg_reaction_time=("reaction_time", "mean")
)

print(summary)

# Bar graph: risk rate by load
summary["risk_rate"].plot(kind="bar")
plt.title("Risk-Taking Rate by Cognitive Load")
plt.ylabel("Proportion of Risky Choices")
plt.xlabel("Cognitive Load Condition")
plt.tight_layout()
plt.savefig("risk_rate_by_load.png")
plt.show()

# Bar graph: reaction time by load
summary["avg_reaction_time"].plot(kind="bar")
plt.title("Average Reaction Time by Cognitive Load")
plt.ylabel("Reaction Time (seconds)")
plt.xlabel("Cognitive Load Condition")
plt.tight_layout()
plt.savefig("reaction_time_by_load.png")
plt.show()

# Simple statistical test
low_rt = df[df["load"] == "Low Load"]["reaction_time"]
high_rt = df[df["load"] == "High Load"]["reaction_time"]

t_stat, p_value = ttest_ind(low_rt, high_rt)

print("\nReaction Time T-Test:")
print("t-statistic:", t_stat)
print("p-value:", p_value)
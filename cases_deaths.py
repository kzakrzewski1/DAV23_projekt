import pandas as pd
import matplotlib.pyplot as plt

can_df = pd.read_csv("owid/can.csv")

can_df["date"] = pd.to_datetime(can_df["date"])

plt.figure(figsize=(25, 8))
ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.plot(
    can_df["date"],
    can_df["new_cases_smoothed"],
    c="blue",
    label="New cases",
    linewidth=2,
)
ax2.plot(
    can_df["date"],
    can_df["new_deaths_smoothed"],
    c="red",
    label="Deaths",
    linewidth=2,
)

plt.grid(True)

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()

ax2.legend(h1 + h2, l1 + l2, fontsize=20)

ax1.set_title("Daily New Cases per 10000 vs Daily Deaths per 1000.000, Canada", size=25)
ax1.set_xlabel("Date", size=18)
ax1.set_ylabel("Number of New Cases\n", size=18)
ax2.set_ylabel("Number of Deaths\n", size=18)
plt.show()

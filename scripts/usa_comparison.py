import pandas as pd
import matplotlib.pyplot as plt
import os

usa_popu = 331.9e6
can_popu = 38.25e6


usa_df = pd.read_csv(os.path.join("data","usa.csv"))
can_df = pd.read_csv(os.path.join("data","can.csv"))

usa_df["date"] = pd.to_datetime(usa_df["date"])
can_df["date"] = pd.to_datetime(can_df["date"])

plt.figure(figsize=(20, 8))
plt.plot(
    can_df["date"],
    can_df["new_cases_smoothed"] / can_popu * 10000,
    c="red",
    label="Canada",
    linewidth=2,
)
plt.plot(
    usa_df["date"],
    usa_df["new_cases_smoothed"] / usa_popu * 10000,
    c="blue",
    label="USA",
    linewidth=2,
)


ax = plt.gca()

ax.set_axisbelow(True)
ax.set_facecolor("#F0F0F0")
ax.grid(color = 'white', linewidth = 1.6)
ax.grid(which = "minor", color = 'white', linewidth = 0.5)
ax.tick_params(labelsize = 14)

ax.legend(fontsize=20)
ax.set_title("Daily New Cases per 10K citizens, Canada vs USA", size=25, pad = 25)
ax.set_xlabel("Date", size=20, labelpad = 17)
ax.set_ylabel("Number of New Cases\n", size=20)


plt.savefig(os.path.join("plots","usa_comparison.png"))
#plt.show()

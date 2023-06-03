import pandas as pd
import matplotlib.pyplot as plt
import os

can_df = pd.read_csv(os.path.join("data","can.csv"))

can_df["date"] = pd.to_datetime(can_df["date"])

plt.figure(figsize=(26, 8))
ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.plot(
    can_df["date"],
    can_df["new_deaths_smoothed"],
    c="red",
    label="Deaths",
    linewidth=2,
)
ax2.plot(
    can_df["date"],
    can_df["new_cases_smoothed"],
    c="blue",
    label="New Cases",
    linewidth=2,
)

ax1.set_ylim(-10, 190)
ax2.set_ylim(-2432, 45600)

ax2.set_yticks(range(0,45600,6000))
ax2.set_yticklabels(["0", "6K", "12K", "18K", "24K", "30K", "36K", "42K"], fontsize = 14)
ax1.tick_params(labelsize = 14)



ax1.set_axisbelow(True)
ax1.set_facecolor("#F0F0F0")
ax1.grid(color = 'white', linewidth = 1.6)
ax1.grid(which = "minor", color = 'white', linewidth = 0.5)

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()

ax2.legend(h1 + h2, l1 + l2, fontsize=20)

ax1.set_title("Daily New Cases vs Daily Deaths", size=25, pad = 25)
ax1.set_xlabel("Date", size=22, labelpad = 17)
ax1.set_ylabel("Number of Deaths\n", size=20)
ax2.set_ylabel("Number of New Cases\n", size=20, labelpad = 30)




plt.savefig(os.path.join("plots","cases_deaths.png"))
#plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import os

can_df = pd.read_csv(os.path.join("data","can.csv"))

can_df["date"] = pd.to_datetime(can_df["date"])

plt.figure(figsize=(20, 8))
plt.plot(
    can_df["date"],
    can_df["new_cases_smoothed"],
    c="red",
    label="Canada",
    linewidth=2,
)

ax = plt.gca()

ax.set_axisbelow(True)
ax.set_facecolor("#F0F0F0")
ax.grid(color = 'white', linewidth = 1.6)
ax.grid(which = "minor", color = 'white', linewidth = 0.5)

ax.set_title("Daily New Cases", size=25, pad = 25)
ax.set_xlabel("Date", size=20, labelpad = 17)
ax.set_ylabel("Number of New Cases\n", size=20)

ax.set_yticks(range(0,41000,10000))
ax.set_yticklabels(["0", "10K", "20K", "30K", "40K"])
ax.tick_params(labelsize = 14)

plt.savefig(os.path.join("plots", "new_cases.png"))
#plt.show()

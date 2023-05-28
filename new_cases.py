import pandas as pd
import matplotlib.pyplot as plt

can_df = pd.read_csv("owid/can.csv")

can_df["date"] = pd.to_datetime(can_df["date"])

plt.figure(figsize=(25, 8))
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
ax.set_xlabel("Date", size=18, labelpad = 15)
ax.set_ylabel("Number of New Cases\n", size=18)
plt.show()

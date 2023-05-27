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
plt.grid(True)
ax = plt.gca()
ax.set_title("Daily New Cases, Canada", size=25)
ax.set_xlabel("Date", size=18)
ax.set_ylabel("Number of New Cases\n", size=18)
plt.show()

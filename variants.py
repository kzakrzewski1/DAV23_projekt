import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


can_df = pd.read_csv("owid/can.csv")
can_df["date"] = pd.to_datetime(can_df["date"])


def get_total(sunday):
    monday = sunday - pd.tseries.offsets.Day(6)
    week_df = can_df[monday <= can_df["date"]]
    week_df = week_df[week_df["date"] <= sunday]
    return week_df["new_cases"].sum()


df = pd.read_csv("covid19-epiSummary-variants.csv")

cols = [
    "Variant Grouping",
    "_Identifier",
    "Lineage Grouped",
    "%CT Count of Sample #",
    "Collection (week)",
]

date = "Collection (week)"
id = "_Identifier"
perc = "%CT Count of Sample #"

df[date] = pd.to_datetime(df[date])
df = df[df[date] != df[date].min()]

omicron = ["Other Omicron", "BA.1", "BA.2", "BA.3", "BA.4", "BA.5"]


def f(x):
    if x in omicron:
        return "Omicron"
    else:
        return x


df[id] = df[id].apply(f)

to_plot = [
    "Omicron",
    "Alpha",
    "Beta",
    "Delta",
    "Gamma",
    "Eta",
    "Other",
    "Recombinants",
]

dates = df[date].unique()
dates = sorted(dates)

scale = [get_total(d) for d in dates]

bottom = np.zeros_like(dates).astype(df[perc].dtype)


plt.figure(figsize=(25, 8))

for x in to_plot:
    tmp = df[df[id] == x]
    tmp = tmp.groupby([date]).sum()
    tmp = tmp.reset_index()
    tmp = tmp.set_index(date)
    tmp = tmp.sort_index()
    tmp = tmp.reindex(dates, fill_value=0)
    plt.bar(dates, scale * tmp[perc], bottom=bottom, width=7.0, label=x)
    bottom += tmp[perc]

ax = plt.gca()
ax.legend(fontsize=16)
ax.set_title("Weekly New Cases per Variant", size=25, pad=25)
ax.set_xlabel("Date", size=18, labelpad=15)
ax.set_ylabel("Total number of New Cases\n", size=18)

ax.set_axisbelow(True)
ax.set_facecolor("#F0F0F0")
ax.grid(color="white", linewidth=1.6)
ax.grid(which="minor", color="white", linewidth=0.5)

plt.show()

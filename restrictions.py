import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("OxCGRT.csv")
df = df[df["CountryCode"] == "CAN"]
df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
df = df[df["StringencyIndex_Average"].notna()]


case_df = pd.read_csv("owid/can.csv")
case_df["date"] = pd.to_datetime(case_df["date"])
case_df = case_df[case_df["new_cases"].notna()]


dates1 = df["Date"].unique()
dates2 = case_df["date"].unique()
dates = list(filter(lambda x: x in dates1, dates2))


case_df = case_df[case_df["date"].isin(dates)]
df = df[df["Date"].isin(dates)]


df = df.groupby(["Date"]).mean()


stringency = "StringencyIndex_Average"

school_closing = "C1M_School closing"

workplace_closing = "C2M_Workplace closing"

public_events = "C3M_Cancel public events"

gatherings = "C4M_Restrictions on gatherings"

public_transport = "C5M_Close public transport"

stay_home = "C6M_Stay at home requirements"

internal_movements = "C7M_Restrictions on internal movement"

international_travel = "C8EV_International travel controls"


def plot(col):
    name = col.split("_")[-1]
    plt.figure(figsize=(25, 8))
    ax1 = plt.gca()
    ax2 = ax1.twinx()

    assert len(case_df["date"]) == len(df.index)

    ax1.plot(
        case_df["date"],
        case_df["new_deaths_smoothed"],
        c="red",
        label="Deaths",
        linewidth=2,
    )
    ax2.plot(df.index, df[col])
    ax1.set_title(f"Daily New Cases vs Restriction severity: {name}", size=25, pad=25)
    ax1.set_xlabel("Date", size=18, labelpad=15)
    ax1.set_ylabel("Number of Deaths\n", size=18)
    ax2.set_ylabel("Restriction severity\n", size=18, labelpad=25)
    plt.show()


def corr(col):
    cases = case_df["new_cases"]
    restriction = df[col]
    #! shifted by 10 days
    cases = cases[10:]
    restriction = restriction[:-10]
    print(np.corrcoef(cases, restriction))


corr(school_closing)
plot(school_closing)

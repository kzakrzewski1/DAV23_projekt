import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os


df = pd.read_csv("data/OxCGRT.csv")
df = df[df["CountryCode"] == "CAN"]
df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
df = df[df["StringencyIndex_Average"].notna()]


case_df = pd.read_csv("data/can.csv")
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
    fig = plt.figure(figsize=(20, 8))
    ax1 = plt.gca()
    

    assert len(case_df["date"]) == len(df.index)

    ax1.plot(
        case_df["date"],
        case_df["new_cases_smoothed"],
        c="blue",
        label="Cases",
        linewidth=2,
    )


    ax1.set_xlim(pd.to_datetime("2020-01-14"), pd.to_datetime('2023-01-04'))

    ax1.pcolorfast(ax1.get_xlim(), ax1.get_ylim(),
              df[col].values[np.newaxis],
              cmap=matplotlib.cm.get_cmap('RdYlGn_r'), alpha=0.4)
    
    


   
    if(name == "Average"):
        ax1.set_title(f"Daily New Cases vs Restriction Index", size=25, pad=25)
    else:
        ax1.set_title(f"Daily New Cases vs Restrictions: {name} ", size=25, pad=25)
    
    ax1.set_xlabel("Date", size=20, labelpad=15)
    ax1.set_ylabel("Number of Cases\n", size=20)
    

    scales = np.linspace(0, 2, 7)
    locs = range(4)
    cmap = plt.get_cmap('RdYlGn_r')
    norm = plt.Normalize(scales.min(), scales.max())

    my_cmap = cmap(np.arange(cmap.N))
    my_cmap[:, -1] = np.linspace(0.499, 0.501, cmap.N)
    my_cmap = matplotlib.colors.ListedColormap(my_cmap)

    sm =  matplotlib.cm.ScalarMappable(norm=norm, cmap=my_cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ticks = [0,2])
    cbar.ax.set_yticklabels(['No restrictions', 'Severe restrictions']) 
    cbar.ax.tick_params(labelsize=14, size = 0) 

    ax1.set_yticks(range(0,41000,10000))
    ax1.set_yticklabels(["0", "10K", "20K", "30K", "40K"])

    ax1.tick_params(labelsize = 13)

    ax1.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=10, maxticks=12))  



    #plt.show()
    plt.savefig(os.path.join("plots", f"Restrictions_{name}"))
    ax1.clear()


def corr(col):
    cases = case_df["new_cases"]
    restriction = df[col]
    #! shifted by 10 days
    cases = cases[10:]
    restriction = restriction[:-10]
    print(np.corrcoef(cases, restriction))

    


corr(international_travel)

plot(international_travel)
plot(stringency)

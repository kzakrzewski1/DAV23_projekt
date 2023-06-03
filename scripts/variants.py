import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot, plot
import numpy as np
from itertools import cycle
import os


can_df = pd.read_csv(os.path.join("data", "can.csv"))
can_df["date"] = pd.to_datetime(can_df["date"])


def get_total(sunday):
    monday = sunday - pd.tseries.offsets.Day(6)
    week_df = can_df[monday <= can_df["date"]]
    week_df = week_df[week_df["date"] <= sunday]
    return week_df["new_cases"].sum()


df = pd.read_csv(os.path.join("data","covid19-epiSummary-variants.csv"))

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

df[date] = pd.to_datetime(df[date],format="%Y-%m-%d")
df = df[df[date] != df[date].min()]

omicron = ["Other Omicron", "BA.1", "BA.2", "BA.3", "BA.4", "BA.5"]


def f(x):
    if x in omicron:
        return "Omicron"
    else:
        return x


df[id] = df[id].apply(f)

to_plot = [
    "Other",
    "Alpha",
    "Beta",
    "Gamma",
    "Delta",
    "Eta",
    "Omicron",
    "Recombinants",
]

dates = df[date].unique()
dates = sorted(dates)

scale = [get_total(d) for d in dates]

bottom = np.zeros_like(dates).astype(df[perc].dtype)


palette = cycle(px.colors.qualitative.Bold)
plots = []
for type in to_plot:
    tmp = df[df[id] == type]
    tmp = tmp.groupby([date]).sum(numeric_only = True)
    tmp = tmp.reset_index()
    tmp = tmp.set_index(date)
    tmp = tmp.sort_index()
    tmp = tmp.reindex(dates, fill_value=0)

    if(type == "Other"):
        name = "Original"
    else:
        name = type

    hovertemplate = f"<b>{name} </b> <br><br>Date: %{{x}} <br>Cases: %{{y:.3s}}<extra></extra>"


    plots.append(go.Bar(x = pd.to_datetime(dates),
                        y =  np.round(scale * tmp[perc],0),
                        name = name, 
                        hovertemplate = hovertemplate,
                        marker_color = next(palette)
                        )
            )
    


layout = go.Layout(
    barmode='stack',
    legend={'traceorder':'normal'}
)

fig = dict(data = plots, layout = layout)
fig = go.Figure(fig)

fig.update_xaxes(dtick = "M3", tickangle = 45, showgrid = True)
fig.update_layout(
    legend=dict(
    title="Variant <br>",
    y = 0.5,
    font=dict(
            family="Courier",
            size=18,
            color="black"
        ),
    ),

    title={
        'text': "<b>Weekly Cases by Variant</b>",
        'y':0.96,
        'x':0.5,
        "font_family": "Courier",
        "font_size": 32,
        'xanchor': 'center',
        'yanchor': 'top'},

    xaxis_range = (pd.to_datetime("2020-03-05"), pd.to_datetime("2023-05-15")),
    yaxis_range = (0,310000),

    yaxis_title={
        'text': "Number of cases",
        "font_family": "Courier",
        "font_size": 26
    },

    xaxis_title={
        'text': "Date",
        "font_family": "Courier",
        "font_size": 26
    }
)

plot(fig, filename = os.path.join("plots","variants.html"))

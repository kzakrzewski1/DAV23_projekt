import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from statsmodels.tsa.holtwinters import ExponentialSmoothing

data = pd.read_csv(os.path.join("data", "travel.csv"), thousands=',')
data["Date"] = pd.to_datetime(data["Date"])

data = data[data["Date"] >= "2015-01-01"].reset_index(drop=True)
data["Visitors_mln"] = data["Visitors"]/1e6



fig, ax = plt.subplots(figsize = (16,8))

ax.plot(data["Date"], data["Visitors_mln"], label = "Actual",  linewidth = 2)

model = ExponentialSmoothing(data.loc[0:61,"Visitors_mln"], seasonal = "add", trend = "add", seasonal_periods = 12)
model_fit = model.fit()

pred = model_fit.predict(62, 98)
pred = list(pred)


visitors_lost = 0
i = 0
for date in data[data["Date"] >= "2020-03-01"]["Date"]:
    difference = pred[i] - data[data["Date"] == date]["Visitors_mln"].values[0]
    visitors_lost += difference
    


pred.insert(0, data[data["Date"] == "2020-02-01"]["Visitors_mln"].values[0])


ax.plot(data[data["Date"] >= "2020-02-01"]["Date"], pred, ls = '--', color = "#CC0066", label = "Forecasted", linewidth = 2.5)
ax.fill_between(data[data["Date"] >= "2020-02-01"]["Date"],
                data[data["Date"] >= "2020-02-01"]["Visitors_mln"],
                pred,
                color = "#FF9999",
                alpha = 0.5
                )

ax.text(pd.to_datetime("2020-04-16"), 1.1, s = f"~{np.round(visitors_lost,1)}M visitors lost", fontsize = 16, weight = "bold")


ax.set_axisbelow(True)
ax.set_facecolor("#F0F0F0")
ax.grid(color = 'white', linewidth = 1.6)
ax.grid(which = "minor", color = 'white', linewidth = 0.5)

ax.set_ylim(-0.1, 5)


ax.set_title("Travelers visiting Canada (monthly)", size=25, pad = 25)
ax.set_xlabel("Year", size=20, labelpad = 15)
ax.set_ylabel("Number of Visitors [mln]\n", size=20)
ax.tick_params(labelsize = 14)

ax.legend(fontsize=18)

plt.savefig(os.path.join("plots", "travel.png"))
#plt.show()


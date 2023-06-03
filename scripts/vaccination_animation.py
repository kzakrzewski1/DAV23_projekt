import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches   
import os
import calendar



data = pd.read_csv(os.path.join("data","vaccinations_provinces.csv"), low_memory=False)
data = data[(data["sex"] == "All sexes") & (data["age"] == "All ages")]
data["week_end"] = pd.to_datetime(data["week_end"])
data["numtotal_fully"].fillna(0, inplace=True)

#data["proptotal_partially"] = 100*data["proptotal_partially"]
#data["proptotal_fully"] = 100*data["proptotal_fully"]


provinces_to_plot = ["Alberta", "British Columbia", "Ontario", "Quebec"]
populations = np.array([4.37e6, 5.07e6, 14.57e6, 8.49e6])



def addlabels(x,y,z):
    y = y.reset_index(drop = True)
    z = z.reset_index(drop = True)
    for i in range(len(x)):
        ax.text(i, z[i]+2, s = f"1 dose: {np.round(z[i],1)}%\n2 doses: {np.round(y[i],1)}%", ha = 'center', fontsize = 13)


def draw_barplot(week):
    
    current = data[data["prename"].isin(provinces_to_plot)][["prename", 
                                                             "week_end",
                                                             "numtotal_atleast1dose",
                                                             "numtotal_fully"]]
    

    current.columns = ["Province", "Date", "Partially Vaccinated", "Fully Vaccinated"]
    current["Partially Vaccinated"] = pd.to_numeric(current["Partially Vaccinated"])
    current["Fully Vaccinated"] = pd.to_numeric(current["Fully Vaccinated"])


    current = current[current["Date"] == week]
    current = current.sort_values("Province")

    provinces, partially_pc, fully_pc = [current["Province"], current["Partially Vaccinated"]*100/populations, 100*current["Fully Vaccinated"]/populations]
    
    ax.clear()
    month = calendar.month_name[week.month]
    year = week.year
    year = str(year)

    ax.bar(provinces, partially_pc)
    ax.bar(provinces, fully_pc, color = "#94143E", alpha = 0.9)
    ax.set_xlabel("Province", fontsize = 20)
    ax.set_ylabel("Vaccination rate", fontsize = 21)
    ax.set_yticks([0,20,40,60,80,100])
    ax.set_yticklabels(["0%", "20%", "40%","60%", "80%", "100%"])
    ax.tick_params(axis='both', which='major', labelsize=14)
    
    ax.set_title("Vaccination rates by", fontsize = 27, pad = 25, ha = "center")
    ax.xaxis.set_label_coords(0.5, -.1)
    ax.yaxis.set_label_coords(-.085, 0.5)
    fig.subplots_adjust(bottom=0.15)
    ax.set_ylim((0,125))

    ax.set_axisbelow(True)
    ax.set_facecolor("#EFEFEF")
    ax.grid(color = 'white', linewidth = 1, zorder = 10)
    ax.grid(which = "minor", color = 'white', linewidth = 0.5)  

    ax.axhline(y=50, linewidth=2, color='green', alpha = 0.6, ls='--', zorder = 0.9)

    if (week == pd.to_datetime("2021-05-29")):
        ax.text(-0.25, 107, s = f"{month} {year}", fontsize = 32, color = "#B70943")
        ax.text(-0.25, 96, s = "Vaccination rates reach over 50%", fontsize = 32, color = "#B70943")
    else:
        ax.text(-0.25, 107, s = f"{month} {year}", fontsize = 32)


    addlabels(provinces_to_plot, fully_pc, partially_pc)

    first_patch = mpatches.Patch(color='blue', label='Partially vaccinated')
    second_patch = mpatches.Patch(color='#94143E', label='Fully vaccinated')

    ax.legend(handles=[first_patch, second_patch], fontsize = 14)
    

animation_frames = []

for date in pd.date_range(start = "2021-01-16", freq="7D", periods = 50):
    animation_frames.append(date)

for i in range(10):
    animation_frames.append(pd.to_datetime("2021-05-29"))

for i in range(12):
    animation_frames.append(pd.to_datetime("2021-12-25"))



animation_frames = sorted(animation_frames)



fig, ax = plt.subplots(figsize=(12, 8))
animator = animation.FuncAnimation(fig, draw_barplot, frames=animation_frames)
writergif = animation.PillowWriter(fps=1.8) 
animator.save(os.path.join("plots", "vaccination.gif"), writer=writergif)

#plt.show()
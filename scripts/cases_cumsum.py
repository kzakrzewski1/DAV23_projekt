import pandas as pd
import os
import numpy as np



data = pd.read_csv(os.path.join("data", "cases_2020_cities.csv"))
lookup = pd.read_csv(os.path.join("data", "health_regions_lookup.csv"))


def change_names(name):
    index = np.argmax(lookup["authority_report_health_region"] == name)
    alternative = lookup.loc[index, "statscan_arcgis_health_region"]

    return(alternative)


data["health_region"] = data["health_region"].apply(change_names)
data['date_report'] = pd.to_datetime(data['date_report'], dayfirst = True)

dates = pd.DataFrame(pd.date_range(start="2020-01-25",end="2020-04-30"))
regions = pd.DataFrame(data["health_region"].unique())

full_dates_regions = dates.merge(regions, how = "cross")


data = data[["provincial_case_id", "health_region", "date_report"]].groupby(["date_report", "health_region"])
data = data.agg("count")


full_dates_regions.columns = ["date_report", "health_region"]

data = full_dates_regions.join(data, on = ["date_report", "health_region"])

data = data.sort_values(["date_report","health_region"])
data = data.fillna(0)

data["cumulative_cases"] = data.groupby("health_region").cumsum()
data.drop(columns = "provincial_case_id", inplace = True)


data.to_csv(os.path.join("data","Map_animation_cases.csv"))

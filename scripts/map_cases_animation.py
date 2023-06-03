import plotly_express as px
import matplotlib
import pandas as pd
import os
import geopandas
import plotly.graph_objects as go
import numpy as np

regions = geopandas.read_file(os.path.join("data","health_regions.geojson"))
data = pd.read_csv(os.path.join("data", "Map_animation_cases.csv"))


regions["lon"] = regions["geometry"].centroid.x
regions["lat"] = regions["geometry"].centroid.y

#print(provinces)
#print(data_total["ratedeaths"])


data = pd.merge(data, regions[["ENG_LABEL", "lon", "lat"]], how = "inner", left_on = "health_region", right_on = "ENG_LABEL")

data.sort_values("date_report", inplace = True)
data = data[data["date_report"] >= "2020-03-14"]


fig = px.scatter_mapbox(data,
                        lat = "lat", lon = "lon",
                        color_continuous_scale="Plasma",
                        color = "cumulative_cases",
                        range_color = [0, 14000],
                        size = "cumulative_cases",
                        size_max = 200,
                        animation_frame = "date_report",
                        #color_discrete_sequence=["#1B0A52","#28529A","#26926E","#C0C61F","#F67708","#FF0A0A"],
                        mapbox_style="mapbox://styles/krzysiekz2901/cli5z1csm000i01qqgfi33c6f",
                        #mapbox_style = "carto-positron",
                        zoom=3.3, center = {"lat": 80.0902, "lon": -150.7129},
                        opacity=0.4,

                        hover_name = "health_region",
                        hover_data = {"lon": False,
                                      "lat": False},

                        labels = {"cumulative_cases": "Total nr of cases ",
                                  "date_report": "Date "},
                        
                        title = "<b>Early spread of the virus in 2020</b>")




mapboxtoken="pk.eyJ1Ijoia3J6eXNpZWt6MjkwMSIsImEiOiJjbGkxaHdzbjYwaGdoM2pvNG5lbHAyYnRtIn0.uOBpelnZlPK7UpymLHT94w"
fig.update_layout(margin={"r":0,"t":60,"l":0,"b":0},  mapbox={"accesstoken":mapboxtoken})
fig.update_mapboxes(bounds_east=-30, bounds_west = -176, bounds_north = 84, bounds_south = 32, center_lon = -92.3, center_lat = 51.5)

fig.update_layout(
    coloraxis_colorbar_title_text = "Confirmed <br>cases <br> <br>",
    coloraxis_colorbar_title_font_family = 'Courier',
    coloraxis_colorbar_title_font_size = 20,
    coloraxis_colorbar_title_side = 'top',

    title=dict(
            x = 0.5,
            xanchor =  'center',
            font_family = "Courier",
            font_size = 32,
        )
    )

fig.write_html(os.path.join("plots", "Map_animation_cases.html"), auto_play = False)

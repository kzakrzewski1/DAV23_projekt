import plotly_express as px
import matplotlib
import pandas as pd
import os
import geopandas
import plotly.graph_objects as go
import numpy as np

provinces = geopandas.read_file(os.path.join("data","georef-canada-province@public.geojson"))
data = pd.read_csv(os.path.join("data", "covidCAN.csv"))

config={
    'displayModeBar': False,
}

#provinces["geometry"] = (
    #provinces.to_crs(provinces.estimate_utm_crs()).simplify(10).to_crs(provinces.crs)
#)

data_total = data.iloc[-15:-2]

#provinces["lon"] = provinces["geometry"].centroid.x
#provinces["lat"] = provinces["geometry"].centroid.y

#print(provinces)
#print(data_total["ratedeaths"])

data_total = data_total.sort_values("ratedeaths")
data_total["bins"] = pd.cut(data_total["ratedeaths"], bins=range(0, 241, 40)).astype(str)


def population_string(population):
    if(population > 1000000):
        population = population / 1000000
        population = np.round(population, 1).astype(str)
        population = population + "M"

        return(population)
    else:
        population = population / 1000
        population = np.round(population, 1).astype(str)
        population = population + "K"

        return(population)
    

data_total["population"] = 100000*data_total["numdeaths"]/data_total["ratedeaths"]
data_total["population"] = data_total["population"].apply(population_string)

data_total.drop(columns = data_total.loc[:,"ratedeaths_last7":"avgratedeaths_last7"], inplace = True)
data_total.drop(columns = data_total.loc[:,"reporting_week":"update"], inplace = True)
data_total.drop(columns = ["numtotal_last7", "numdeaths_last7", "ratecases_last7"], inplace = True)
data_total.to_csv(os.path.join("data", "Map_data_deaths_100k.csv"))



fig = px.choropleth_mapbox(data_total, geojson=provinces, 
                           featureidkey = "properties.prov_name_en", locations='prname',
                           #color_continuous_scale="Viridis",
                           color="bins",
                           color_discrete_sequence=["#1B0A52","#28529A","#26926E","#C0C61F","#F67708","#FF0A0A"],
                           mapbox_style="mapbox://styles/krzysiekz2901/clicziusb002j01qp7jjcd4qh",
                           zoom=3.14, center = {"lat": 80.0902, "lon": -150.7129},
                           opacity=0.60,
                           hover_name = "prname",
                           hover_data = {"prname": False,
                                         "bins": False,
                                         "ratedeaths" : True,
                                         "population": True},

                            labels = {"ratedeaths": "Deaths per 100K ",
                                      "population": "Population "},        
                            title = "<b>Deaths per 100K people by province</b>"                    
                          )


mapboxtoken="pk.eyJ1Ijoia3J6eXNpZWt6MjkwMSIsImEiOiJjbGkxaHdzbjYwaGdoM2pvNG5lbHAyYnRtIn0.uOBpelnZlPK7UpymLHT94w"
fig.update_layout(margin={"r":0,"t":60,"l":0,"b":0},  mapbox={"accesstoken":mapboxtoken})
fig.update_mapboxes(bounds_east=-30, bounds_west = -176, bounds_north = 84, bounds_south = 32, center_lon = -96, center_lat = 56.6)

fig.update_layout(
    legend=dict(
    title="Deaths per <br>100k people <br>",
    y = 0.5,
    font=dict(
            family="Courier",
            size=18,
            color="black"
        ),
    ),

    title=dict(
            x = 0.5,
            xanchor =  'center',
            font_family = "Courier",
            font_size = 32,
        )
    )

fig.write_html(os.path.join("plots", "Map_deaths_100K.html"))

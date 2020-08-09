"""
Created on Sat Ago 08 2020
Density Heatmap con información de los sismos ocurridos en Venezuela en los últimos años.
@author: bellorinp
"""

import pathlib
import pandas as pd
import plotly.express as px

#Data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

#DataFrame
df = pd.read_csv(DATA_PATH.joinpath('sismos_ven.csv')

#Pasar la columna Fechas a datetime (Hora Local)
df.Fecha = pd.to_datetime(df.Fecha, format='%Y/%m/%d %H:%M:%S').dt.tz_convert('America/Caracas')

#Agregar un columna de año en función de la fecha del evento
df['Año'] = pd.DatetimeIndex(df['Fecha']).year

#Agregar un columna de tiempo del evento
df['Tiempo'] = pd.DatetimeIndex(df['Fecha']).time
df['Tiempo'] = df['Tiempo'].apply(lambda x: x.replace(microsecond=0))#reemplazar milisegundos

#Remover el tiempo a la columna fecha
df.Fecha = df.Fecha.dt.date

#Densitymap
fig = px.density_mapbox(df, lat='Latitud', lon='Longitud', z='Magnitud', 
                        radius=12, opacity=0.6, 
                        center=dict(lat=8.889, lon=-66.71), zoom=5,
                        hover_name='Lugar',
                        hover_data=['Magnitud', 'Escala de Magnitud', 'Fecha', 'Tiempo'],
                        animation_frame='Año',
                        title='Sismos Ocurridos en Venezuela (2000-2020)',
                        mapbox_style='white-bg',
                        color_continuous_scale='ylorrd'
                       )

fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0},
                  mapbox_layers=[
                            {"below": 'traces',
                             "sourcetype": "raster",
                             "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"]}
                        ],
                  annotations = [dict(x=0.01,
                                      y=0.01,
                                      xref='paper',
                                      yref='paper',
                                      font=dict(color="black",
                                                size=10),
                                      bgcolor='white',
                                      text='<b>Fuente:</b> Servicio Geológico de Estados Unidos (USGS)',
                                      showarrow = False
                                     )]
                 )

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1200
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1200
fig.layout.sliders[0].pad.t = 10

fig.show()

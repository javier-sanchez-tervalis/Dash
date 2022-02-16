# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 13:15:29 2021

@author: Marie-charlotte
"""

import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
import plotly.graph_objects as go


@st.experimental_memo
def read_csv(path):
    return(pd.read_csv(path))


# Import du csv propre==========================================================

df = read_csv("data.csv")


# 1/ Surface brulée par état et par années =====================================

sur = pd.read_csv('surface_brulee_etat_annee.csv')  # CSV différent de Data
bar = px.bar(sur, x='State', y='Surface', animation_frame='fire_year',
             color='State',
             labels={'State': 'Etat', 'Surface': 'Surface brulée en km2',
                     'fire_year': 'Année'},
             range_y=[0, 30000],
             title= "Surface brulée par année pour les 10 états les plus touchés par "
                      "les feux de forêt", 
             width=800,
             height=500)

st.write(bar)


# 2/ Nombre de feux=============================================================

df2 = df.loc[df['state'].isin(['Alaska', 'California', 'Idaho', 'Texas', 'Nevada', 'Montana',
                               'Arizona', 'Washington', 'Oregon', 'New Mexico'])]
nbr = pd.crosstab(df2['fire_year'],
                  df2['state'])
#
fig1 = px.line(nbr,
               labels={'fire_year': 'Année',
                       'state': 'Etat',
                       'value': 'Nombre de feux'}, 
               title = "Evolution du nombre de feux par an pour les 10 états les plus "
                         "touchés par les feux de forêt", 
               width=800,
               height=500)
st.write(fig1)


# 2/ Nombre de feux par taille par année----------------------------------------

dic = dict({})
classe = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

for i in classe:
    dic[i] = df.loc[df['fire_size_class'].isin([i])].groupby('fire_year').agg(
        {'size_km2': 'sum'}).rename(columns={"size_km2": str(i)})
dfclass = dic['A'].append(dic['B']).append(dic['C']).append(
    dic['D']).append(dic['E']).append(dic['F']).append(dic['G'])
fig2 = px.line(dfclass,
               labels={'value': 'Surface brulée (km2)',
                       'fire_year': 'Année',
                       'variable': 'Classe de feu'},
               title='Surface brulée par année par classe de feu',
               width=800,
               height=500)

st.write(fig2)


# 3/ Clustering Surveillance feux================================================
data = df.loc[df['fire_size_class'].isin(['G'])]
data1 = data.drop(['fire_year', 'discovery_date', 'discovery_doy', 'stat_cause_code',
                   'stat_cause_descr', 'cont_date', 'cont_doy', 'fire_size',
                   'fire_size_class', 'state', 'size_km2',
                   'climat', 'Température'], axis=1)

nbr = [10, 20, 30, 50, 75, 100]

centre = st.selectbox("Nombre de centre d'intervention",
                      [10, 20, 30, 50, 75, 100])


for i in nbr:
    if centre == i:
        kmeans = KMeans(n_clusters=i)

        kmeans.fit(data1)
        centroids = kmeans.cluster_centers_

fig3 = go.Figure()
fig3.add_trace(go.Scattergeo(
    locationmode='USA-states',
    lon=centroids[:, 1],
    lat=centroids[:, 0],
    name="Centre de surveillance",
    marker=dict(
        size=20,
        color='#01665e',
        line_color='rgb(40,40,40)',
        sizemode='area',
        opacity=0.5,
    ),))
fig3.add_trace(go.Scattergeo(
    locationmode='USA-states',
    lon=data['longitude'],
    lat=data['latitude'],
    name='Feux G',
    marker=dict(
        size=5,
        color='red',
        line_color='rgb(40,40,40)',
        sizemode='area',
        opacity=0.1,
    ),))
fig3.update_layout(
    title_text="Surface de surveillance et d'action des centres"
    " (rayon d'action = 100 km)",
    showlegend=True,
    geo=dict(
        scope='usa',
        landcolor='rgb(217, 217, 217)',
    ),
    width=1000,
    height=500,  #Ne pas changer la taille
)
st.write(fig3)


# 4/ Nombre de feux / Température ================================================

# Données de température
temp = pd.read_csv('raw_data/climatology1991_2015.csv', header=1, index_col=0)
temp = temp.loc[1992:2015]

d = dict({'California': list()})
top5 = ['Alaska', 'California', 'Idaho', 'Oregon', 'Texas']
for i in top5:
    d[i] = pd.DataFrame(df.loc[df['state'].isin([i]) & df['stat_cause_descr'].isin(
        ['Lightning'])]['fire_year'].value_counts())
    d[i] = d[i].join(df.loc[df['state'].isin([i]) & df['stat_cause_descr'].isin(
        ['Lightning'])].groupby('fire_year').agg({'size_km2': 'sum'}))
    d[i] = d[i].reset_index()
    d[i] = d[i].sort_values('index').merge(pd.DataFrame(temp[i]).reset_index())
    d[i] = d[i].rename(columns={'index': 'année',
                       'fire_year': 'nbr_feux',
                                i:  'température'})
    d[i]['state'] = (i)


tempe = d['Alaska'].append(d['California']).append(
    d['Idaho']).append(d['Oregon']).append(d['Texas'])
tempe = tempe.rename(columns={'nbr_feux': 'Nombre de feux',
                              'température': 'Température (°C)',
                              'state':  'Etat',
                              'size_km2': 'Surface (km²)'})

# Affichage du bubble plot
fig4 = px.scatter(tempe, x="Température (°C)", y="Nombre de feux", size='Surface (km²)', color='Etat',
                  size_max=60,
                  # size="pop", color="continent",
                  hover_name="année", 
                  width=800,
                  height=500)

fig4.update_layout(
    title='Nombre de feux et surface brulée en fonction de la température',
    xaxis=dict(
        title='Température (°C)',
    ),
    yaxis=dict(
        title='Nombre de feux',
    ),
    legend=dict(
        title='Etats',)
    
)


st.write(fig4)

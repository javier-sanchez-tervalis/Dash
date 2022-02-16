import streamlit as st
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import plotly.express as px
from plotly_express import data, scatter_mapbox
from PIL import Image
from sklearn.cluster import KMeans
import plotly.graph_objects as go


#============= set-up du streamlit ====================================================================
st.set_page_config(page_title="dataviz wildfire USA",
                   page_icon=None,
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None)


#============= Création de la BARRE LATERALE =============================================================
st.sidebar.image('roadsignFire.png')
st.sidebar.header("Exploration ")
st.sidebar.markdown('---')


#============ Création du menu déroulant pour faire apparaître les différentes pages ======================

st.sidebar.write("Sélectionnez les thématiques à explorer")
menu = st.sidebar.selectbox(" Enjoy and have fun ! ",
                        ["Intro",
                         "Année",
                         "Cause des feux",
                         "Surfaces brûlées",
                         "Nombre de feux",
                         "Classes de feux",
                         "MachineLearning"]
                        )


st.sidebar.markdown('---')
st.sidebar.write(" Créé par :")
st.sidebar.write("Manon | Marie-Charlotte | Martin")

#======== Mise en place de st.experimental_memo pour accélerer le streamlit =======
@st.experimental_memo
def read_csv(path):
    return(pd.read_csv(path))

perfect = read_csv("perfectData.csv")
df = read_csv("data.csv")
sun = pd.read_csv("sunData.csv")

#======= Code contenant les différentes pages ====================================
if menu == 'Intro':


    # photo d'accueil
    image = Image.open('camion.png')
    st.image(image, caption='Wildfire in the US')

    st.title("Feux de Forets aux Etats-Unis")

    st.header("Présentation des données")

    #création du DataFrame df
    st.write("Cette analyse s'appuie sur un jeu de données baptisé Fire Program Analysis Fire-occurrence Database (FPA FOD) qui recueille  les données des organisations fédérales, nationales et locales Américaines et recense l'intégralité des 1,88 million de feux  survenus de 1992 à 2015.")
    st.write(" En 24 ans, ces feux ont détruit  plus de 500 000km2 sur l'ensemble des 52 Etats Américains.")
    st.write()
    st.markdown('---')
    st.write()
    st.write("Extrait du dataframe, limité à 1000 lignes, et aux colonnes les plus importantes pour l'analyse")
    st.dataframe(perfect.head(1000))
    st.write()
    st.markdown("---")

    #video de fin
    video_file = open(' California wildfire.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)


#============ PAGE ANNEE ===================================
elif menu == 'Année':
    st.title("Feux par année, Etats et classe")

    st.write("Ce Sunburst vous permet de naviguer à travers les données. Cliquez pour naviguer dans la section désirée")
    st.write("Les états avec la plus grande surface brulée sont mis en avant.")

    #création du csv

    # Création du SUNBURST
    fig = px.sunburst(sun,
                      path=['state', 'fire_year', 'fire_size_class'],
                      values="size_km2",
                      color="fire_number",
                      color_continuous_scale="Turbo",
                      range_color=(0, 100),
                      width=1000,
                      height=800)

    st.plotly_chart(fig, use_container_width=True)


#========= PAGE CAUSE DES FEUX ===============================================
elif menu == 'Cause des feux':

    st.title("Causes des incendies")
    st.markdown("---")

    st.subheader("En fonction des années")

    st.write('')
    st.write(
        "La taille des ronds prend en compte la surface brûlée en km2 et la couleur correspond à la cause d'origine de l'incendie.")
    st.write(
        "*En déplaçant le curseur vous pourrez remarquer que les feux sont présents sur l'ensemble du territoire Américain, et pourtant, "
        "ils ne sont pas visibles sur la carte. En effet, la plupart des incendies n'ont eu qu'un impact très léger en terme de surface "
        "brûlée. Les bulles visibles ci-dessous attestent la présence d'incendies aux dégâts conséquents.*")

    # REPRESENTATION GEOGRAPHIQUE
    ## MAP1 1992-2003
    st.write('**Carte des incendies aux Etats-Unis de 1992 à 2003**')

    dfcause1 = perfect[perfect["fire_year"] <= 2003]
    df_sorted_year1 = dfcause1.sort_values(by='fire_year')

    df_geo = data.carshare()
    fig_cause1 = px.scatter_mapbox(df_geo,
                                   lat=df_sorted_year1.latitude,
                                   lon=df_sorted_year1.longitude,
                                   color=df_sorted_year1.stat_cause_descr,
                                   color_discrete_sequence=['lightgreen', 'blue', 'green', 'grey', 'black', 'red',
                                                            'yellow', 'darkblue', 'darkorange', 'lightblue', 'pink',
                                                            'cyan', 'magenta'],
                                   size=df_sorted_year1.size_km2,
                                   size_max=35,
                                   zoom=2,
                                   animation_frame=df_sorted_year1.fire_year,
                                   mapbox_style="stamen-terrain",
                                   width =1000,
                                   height =800)  #

    st.plotly_chart(fig_cause1, use_container_width=True)

    st.write('')
    st.write('**Carte des incendies aux Etats-Unis de 2004 à 2015**')

    ## MAP2 2004-2015

    dfcause2 = perfect[perfect["fire_year"] > 2003]
    df_sorted_year2 = dfcause2.sort_values(by='fire_year')

    fig_cause2 = px.scatter_mapbox(df_geo,
                                   lat=df_sorted_year2.latitude,
                                   lon=df_sorted_year2.longitude,
                                   color=df_sorted_year2.stat_cause_descr,
                                   color_discrete_sequence=['grey', 'blue', 'yellow', 'red', 'lightgreen', 'black',
                                                            'green', 'darkorange', 'darkblue', 'magenta', 'lightblue',
                                                            'cyan', 'pink'],
                                   size=df_sorted_year2.size_km2,
                                   size_max=35,
                                   zoom=2,
                                   animation_frame=df_sorted_year2.fire_year,
                                   mapbox_style="stamen-terrain",
                                   width =1000,
                                   height=800)  #

    st.plotly_chart(fig_cause2, use_container_width=True)

    # REPRESENTATION PAR MOIS
    st.subheader("En fonction des mois")

    perfect_sorted = perfect.sort_values(by='fire_year')
    figviolon = px.violin(perfect_sorted,
                          x='discovery_doy', y="stat_cause_descr",
                          points=False,
                          color='stat_cause_descr',
                          labels={
                              "discovery_doy": "Mois",
                              "stat_cause_descr": "Causes d'incendies",
                              "stat_cause_descr": "Légende"
                          },
                          color_discrete_sequence=['aquamarine', 'darkorange', 'darkgreen', 'grey', 'black', 'red',
                                                   'yellow', 'darkblue', 'lightgreen',
                                                   'lightblue', 'pink', 'blue', 'magenta'],
                          range_x=[0, 366],
                          width=800,
                          height=800,
                          animation_frame=perfect_sorted['fire_year'],
                          orientation='h',
                          )
    figviolon.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 31, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336],
            ticktext=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août',
                      'Septembre', 'Octobre', 'Novembre', 'Décembre'],

        )
    )
    figviolon.update_traces(width=2)

    st.plotly_chart(figviolon, use_container_width=True)


#======== PAGE SURFACES BRULEES ==============================================
elif menu == 'Surfaces brûlées':
    st.title("Surfaces brûlées")

    # Création du dataframe
    burned = pd.read_csv("burnedData.csv")
    # création du PIE
    fig_pie = px.pie(burned,
                     values='size_km2',
                     names='fire_size_class',
                     color_discrete_sequence=["DarkRed",
                                              "firebrick",
                                              "OrangeRed",
                                              "DarkOrange",
                                              "orange",
                                              "Gold",
                                              "yellow"
                                              ],
                     title="surfaces totales brulées par classe de feux de 1992 à 2015",
                     width=1000,
                     height=800
                     )
    st.plotly_chart(fig_pie, use_container_width=True)

    sur = pd.read_csv('surface_brulee_etat_annee.csv')  # CSV différent de Data
    bar = px.bar(sur, x='State', y='Surface', animation_frame='fire_year',
                 color='State',
                 labels={'State': 'Etat', 'Surface': 'Surface brulée en km2',
                         'fire_year': 'Année'},
                 range_y=[0, 30000],
                 title= "Surfaces brulées par année pour les 10 états les plus touchés par "
                          "les feux de forêt",
                 width=1000,
                 height=800)

    st.plotly_chart(bar, use_container_width=True)

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
                   title='Surfaces brulées par année par classe de feux',
                   width=1000,
                   height=800)

    st.write(fig2)


#========= Nombre de feux=============================================================
    #1: VARIATION POUR LE TOP 10
elif menu == 'Nombre de feux':
    st.title("Nombre de feux")

    df2 = df.loc[df['state'].isin(['Alaska', 'California', 'Idaho', 'Texas', 'Nevada', 'Montana',
                                   'Arizona', 'Washington', 'Oregon', 'New Mexico'])]
    nbr = pd.crosstab(df2['fire_year'],
                      df2['state'])
    #
    fig1 = px.line(nbr,
                   labels={'fire_year': 'Année',
                           'state': 'Etat',
                           'value': 'Nombre de feux'},
                   title="Evolution du nombre de feux par an pour les 10 états les plus "
                         "touchés par les feux de forêt",
                   width=1000,
                   height=800)
    st.write(fig1)

    #2/ graph température / nombre de feux
    # Données de température
    temp = pd.read_csv('climatology1991_2015.csv', header=1, index_col=0)
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
                                    i: 'température'})
        d[i]['state'] = (i)

    tempe = d['Alaska'].append(d['California']).append(
        d['Idaho']).append(d['Oregon']).append(d['Texas'])
    tempe = tempe.rename(columns={'nbr_feux': 'Nombre de feux',
                                  'température': 'Température (°C)',
                                  'state': 'Etat',
                                  'size_km2': 'Surface (km²)'})

    # Affichage du bubble plot
    fig4 = px.scatter(tempe, x="Température (°C)", y="Nombre de feux", size='Surface (km²)', color='Etat',
                      size_max=60,
                      # size="pop", color="continent",
                      hover_name="année",
                      width=1000,
                      height=800)

    fig4.update_layout(
        title='Nombre de feux et surface brulée en fonction de la température',
        xaxis=dict(
            title='Température (°C)',
        ),
        yaxis=dict(
            title='Nombre de feux',
        ),
        legend=dict(
            title='Etats', )

    )

    st.write(fig4)

    sun2 = sun.drop(['fire_year', 'fire_size_class', 'USA'], axis=1)
    df_tree = sun2.groupby("state").agg({"size_km2": "sum", "fire_number": "sum"})
    df_tree = df_tree.reset_index()

    df = px.data.gapminder()
    tree_fig = px.treemap(df_tree,
                     path=['state'],
                     values='size_km2',
                     color='fire_number',
                     title='nombre de feux et surface détruites au bout de 24 ans',
                     width=1000,
                     height=800)
    st.plotly_chart(tree_fig,use_container_width=True)




elif menu == 'Classes de feux':
    st.title("Classes de feux")

    ###affichage du code pour la MAP

    # Création de la MAP
    df.sort_values(by="fire_size_class", ascending=True)
    df_geo = px.data.carshare()
    fig_map = px.scatter_mapbox(df_geo,
                                lat=df.latitude,
                                lon=df.longitude,
                                color=df.fire_size_class,
                                color_continuous_scale=['#0d0887',
                                                        '#46039f',
                                                        '#7201a8',
                                                        '#9c179e',
                                                        '#bd3786',
                                                        '#d8576b',
                                                        '#ed7953'],
                                zoom=10,
                                animation_frame=df.fire_year,
                                opacity=0.5,
                                mapbox_style="open-street-map",
                                width=1000,
                                height=800,
                                title= "Carte des feux aux USA par classe de feux"
                                )
    st.plotly_chart(fig_map, use_container_width=True)

elif menu == 'MachineLearning' :
    st.header("Machine Learning")

    #== Clustering Surveillance feux================================================
    st.subheader("Emplacement idéal des super-casernes pour combattre les deux de classe G")

    data = df.loc[df['fire_size_class'].isin(['G'])]
    data1 = data.drop(['fire_year', 'discovery_date', 'discovery_doy', 'stat_cause_code',
                       'stat_cause_descr', 'cont_date', 'cont_doy', 'fire_size',
                       'fire_size_class', 'state', 'size_km2',
                       'climat', 'Température'], axis=1)

    nbr = [10, 20, 30, 50, 75, 100]

    centre = st.selectbox("Nombre de centres d'intervention",
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
        ), ))
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
        ), ))
    fig3.update_layout(
        title_text="Surface de surveillance et d'action des centres"
                   " (rayon d'action = 100 km)",
        showlegend=True,
        geo=dict(
            scope='usa',
            landcolor='rgb(217, 217, 217)',
        ),
        width=1000,
        height=500,  # Ne pas changer la taille
    )
    st.write(fig3)

    # 2nd machine learning :
    ## Titres et image
    st.subheader("Machine learning : Prédire la cause de l'incendie")

    image = Image.open("mage.png")

    st.image(image, width=50)

    st.write("Est-il possible de prédire la cause d'un incendie de manière générale ?")

    ## Mise en place des boutons "Score"
    import time

    Score1 = 0.4960554969116681
    Score2 = 0.6307801527813599

    if st.button('Score'):
        time.sleep(1)
        st.write(Score1)
        st.write(
            "*La précision de l'algorithme laisse à désirer... Peut-être que le nombre de causes dans notre jeu de données est trop élevé ?*")
        st.write(
            "*Et si on décide de placer les 13 causes dans seulement 4 catégories, quelle sera la précision de notre algorithme ?*")
        st.write("**Appuie sur le bouton ci-dessous pour connaître la réponse**")
    if st.button('Nouveau score'):
        time.sleep(1)
        st.write(Score2)
        st.write("*Le score est amélioré grâce à la catégorisation des données*")
    st.write("Est-il possible de prédire les incendies d'origines criminelles ?")
    Score3 = 0.852860861542225
    if st.button('Score :'):
        time.sleep(1)
        st.write(Score3)

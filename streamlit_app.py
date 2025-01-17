import streamlit as st
import pandas as pd
from main import *

# Crear un título para la aplicación
st.title('Streaming Services')

# Cargar los datos en la app
All = pd.read_csv("data/all.csv")
Score = pd.read_parquet('data/score.parquet')

# Definir las funciones para las consultas
# Query 1: Duracion maxima
def get_max_duration(year:int, platform:str, duration_type:str): 
    Q1 = All[(All['platform'] == platform) & (All['release_year'] == year) & (All['duration_type'] == duration_type)].sort_values(by = 'duration_int' , ascending=False)
    if len(Q1) > 0:
        max_duration_title = Q1['title'].values[0]
        return max_duration_title
    else: 
        return ("Not titles found with those parameters.")
# Query 2: Titulos por puntuacion
def get_score_count(platform:str, scored:int, year:int):
    Q2 = Score[(Score['platform'] == platform) & (Score['score'] >= scored) & (All['release_year'] == year)].shape[0]
    # if len(Q2) > 0: 
    return Q2
    # else:
    #     return (0)
# Query 3: Titulos por plataforma
def get_count_platform(platform:str):
    All_platform = All.loc[All['platform'] == platform]
    movies_platform = len(All_platform.index)
    return movies_platform
# Query 4: Actor con mas apariciones
def get_actor(platform:str, year:int):
    Q4_1 = All[(All['platform'] == platform) & (All['release_year'] == year)]   # Filtra por plataforma y anio
    if len(Q4_1) > 0: 
        Q4_2 = Q4_1.assign(actor=Q4_1.cast.str.split(',')).explode('cast')          # Divide 'cast', crea y cuenta una fila por cada elemento.
        Q4_3 = Q4_2.cast.value_counts()  
        max_actor = Q4_3.index[0]                                                   # Obtiene el actor con más apariciones y número de apariciones
        max_count = int(Q4_3.iloc[0])
        Q4 = dict({'actor': max_actor, 'appearances': max_count})
        return Q4
    else:
        return ({})
    


# Crear un título para la aplicación
st.title('Consultas de películas y series')

# Opciones de consulta
options = ['Inicio','Duración máxima', 'Títulos por puntuación', 'Títulos por plataforma', 'Actor con más apariciones']
query = st.sidebar.selectbox('Seleccione una consulta', options)

if query == 'Inicio':
         st.write('Bienvenido a la aplicación de consultas en el catálogo de servicios de streaming')

# Consulta 1: Duración máxima
if query == 'Duración máxima':
    st.subheader('Duración máxima por año y plataforma')
    year = st.number_input('Año', min_value=2000, max_value=2023, value=2020, step=1)
    platform = st.selectbox('Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    duration_type = st.selectbox('Tipo de duración', ['min', 'season'])
    if st.button('Consultar'):
        result = get_max_duration(year, platform, duration_type)
        if isinstance(result, str):
            st.write(f'La duración máxima en {duration_type.lower()}s en {year} en {platform} es: {result}.')
        else:
            st.write(result)

# Consulta 2: Títulos por puntuación
if query == 'Títulos por puntuación':
    st.subheader('Títulos con una puntuación dada en una plataforma y año determinados')
    platform = st.selectbox('Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    scored = st.number_input('Puntuación mínima', min_value=1.0, max_value=5.0, value=3.5, step=0.5)
    year = st.number_input('Año', min_value=2000, max_value=2023, value=2020, step=1)
    if st.button('Consultar'):
        result = get_score_count(platform, scored, year)
        st.write(f'Hay {result} títulos en {platform} con una puntuación de {scored} o más en {year}.')

# Consulta 3: Títulos por plataforma
if query == 'Títulos por plataforma':
    st.subheader('Número de títulos en una plataforma dada')
    platform = st.selectbox('Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    if st.button('Consultar'):
        result = get_count_platform(platform)
        st.write(f'Hay {result} títulos en {platform}.')



# Consulta 4: Actor con más apariciones
if query == 'Actor con más apariciones':
    st.subheader('Actor con más apariciones en una plataforma y año determinados')
    platform = st.selectbox('Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    year = st.number_input('Año', min_value=2000, max_value=2022, value=2020, step=1)
    if st.button('Consultar'):
        result = get_actor(platform, year)
        if isinstance(result, str):
            st.write(result)
        else:
            st.write(f'El actor con más apariciones en {platform} en {year} es {result["actor"]}, con {result["appearances"]} apariciones.')




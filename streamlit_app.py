import streamlit as st
import pandas as pd
import numpy as np
from fastapi import FastAPI
# Crear la aplicación
app = FastAPI()

# Crear un título para la aplicación
st.title('Mi primera aplicación de Streamlit')

# Cargar los datos en la app
All = pd.read_csv("data/all.csv")
Score = pd.read_parquet('data/score.parquet')

# Definir las funciones para las consultas
# Query 1: Duracion maxima
def get_max_duration(year:int, platform:str, duration_type:str): 
    Q1 = All[(All['platform'] == platform) & (All['release_year'] == year) & (All['duration_type'] == duration_type)].sort_values(by = 'duration_int' , ascending=False)
    max_duration_title = Q1['title'].values[0]
    return max_duration_title
# Query 2: Titulos por puntuacion
def get_score_count(platform:str, scored:int, year:int):
    result = Score[(Score['platform'] == platform) & (Score['score'] >= scored) & (All['release_year'] == year)].shape[0]
    return result
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
        return ("No actor found with those parameters.")
    
# Aplicación de Streamlit: # Query 3: Titulos por plataforma
st.title('Consulta titulos por plataforma')

# Formulario para ingresar los parámetros
platform = st.text_input('Plataforma')

# Botón para realizar la consulta y mostrar los resultados
if st.button('Consultar'):
    result = get_actor(platform)
    st.write(f"La cantidad te titulos en la plataforma {platform} es {result}.")

# Aplicación de Streamlit: # Query 4: Actor con mas apariciones
st.title('Consulta de actores')

# Formulario para ingresar los parámetros
platform = st.text_input('Plataforma')
year = st.number_input('Año', value=2022, step=1)

# Botón para realizar la consulta y mostrar los resultados
if st.button('Consultar'):
    result = get_actor(platform, year)
    st.write(f"El actor con más apariciones en la plataforma {platform} en el año {year} es {result['actor']} con {result['appearances']} apariciones.")


# Crear la aplicación de Streamlit
def app():
    st.title('Consultas en el catálogo de películas')
    menu = ['Inicio', 'Máxima duración', 'Puntuación', 'Cantidad de películas', 'Actores']
    choice = st.sidebar.selectbox('Seleccione una consulta', menu)

    if choice == 'Inicio':
        st.write('Bienvenido a la aplicación de consultas en el catálogo de películas')

    elif choice == 'Máxima duración':
        st.subheader('Película con mayor duración')
        year = st.number_input('Ingrese el año', min_value=1900, max_value=2025)
        platform = st.selectbox('Seleccione la plataforma', All['platform'].unique())
        duration_type = st.selectbox('Seleccione el tipo de duración', All['duration_type'].unique())
        if st.button('Buscar'):
            max_duration_title = get_max_duration(year, platform, duration_type)
            if max_duration_title:
                st.write(f"La película con mayor duración en {year} en la plataforma {platform} y con duración tipo {duration_type} es {max_duration_title}")
            else:
                st.write(f"No se encontró ninguna película con los criterios de búsqueda especificados.")


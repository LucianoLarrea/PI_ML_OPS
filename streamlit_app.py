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
        return ({})
    


# Crear un título para la aplicación
st.title('Consultas de películas y series')

# Opciones de consulta
options = ['Inicio','Duración máxima', 'Títulos por puntuación', 'Títulos por plataforma', 'Actor con más apariciones']
query = st.sidebar.selectbox('Seleccione una consulta', options)

if query == 'Inicio':
         st.write('Bienvenido a la aplicación de consultas en el catálogo de películas')

# Consulta 1: Duración máxima
if query == 'Duración máxima':
    st.subheader('Duración máxima por año y plataforma')
    year = st.number_input('Año', min_value=2000, max_value=2023, value=2020, step=1)
    platform = st.selectbox('Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    duration_type = st.selectbox('Tipo de duración', ['min', 'season'])
    if st.button('Consultar'):
        result = get_max_duration(year, platform, duration_type)
        if isinstance(result, str):
            st.write(f'La duración máxima en {duration_type.lower()}s en {year} en {platform} es {result}.')
        else:
            st.write(result)

# Consulta 2: Títulos por puntuación
if query == 'Títulos por puntuación':
    st.subheader('Títulos con una puntuación dada en una plataforma y año determinados')
    platform = st.selectbox('Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    scored = st.number_input('Puntuación mínima', min_value=1, max_value=5, value=3, step=0.1)
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

      

    
# # Aplicación de Streamlit: # Query 3: Titulos por plataforma
# st.title('Consulta titulos por plataforma')

# # Formulario para ingresar los parámetros
# platform = st.text_input('Plataforma')

# # Botón para realizar la consulta y mostrar los resultados
# if st.button('Consultar'):
#     result = get_count_platform(platform)
#     st.write(f"La cantidad te titulos en la plataforma {platform} es {result}.")

# # Aplicación de Streamlit: # Query 4: Actor con mas apariciones
# st.title('Consulta de actores')

# # Formulario para ingresar los parámetros
# platform = st.text_input('Plataforma')
# year = st.number_input('Año', value=2022, step=1)

# # Botón para realizar la consulta y mostrar los resultados
# if st.button('Consultar'):
#     result = get_actor(platform, year)
#     st.write(f"El actor con más apariciones en la plataforma {platform} en el año {year} es {result['actor']} con {result['appearances']} apariciones.")


# # Crear la aplicación de Streamlit
# def app():
#     st.title('Consultas en el catálogo de películas')
#     menu = ['Inicio', 'Máxima duración', 'Puntuación', 'Cantidad de películas', 'Actores']
#     choice = st.sidebar.selectbox('Seleccione una consulta', menu)

#     if choice == 'Inicio':
#         st.write('Bienvenido a la aplicación de consultas en el catálogo de películas')

#     elif choice == 'Máxima duración':
#         st.subheader('Película con mayor duración')
#         year = st.number_input('Ingrese el año', min_value=1900, max_value=2025)
#         platform = st.selectbox('Seleccione la plataforma', All['platform'].unique())
#         duration_type = st.selectbox('Seleccione el tipo de duración', All['duration_type'].unique())
#         if st.button('Buscar'):
#             max_duration_title = get_max_duration(year, platform, duration_type)
#             if max_duration_title:
#                 st.write(f"La película con mayor duración en {year} en la plataforma {platform} y con duración tipo {duration_type} es {max_duration_title}")
#             else:
#                 st.write(f"No se encontró ninguna película con los criterios de búsqueda especificados.")


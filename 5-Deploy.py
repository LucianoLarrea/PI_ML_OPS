# Filtra por anio, plataforma, duration_type y da un listado de peliculas
# Al seleccionar una pelicula devuelve el porcentaje de recomendacion
import streamlit as st
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import time

# Cargar modelo entrenado desde el archivo
# with open('model.pkl', 'rb') as file:
#     model = pickle.load(file)

# Crear un título para la aplicación
st.set_page_config(page_title='Streaming Services') # Nombre para configurar la pagina web
st.header('Consultas de títulos de streaming') # Titulo de la pagina

# Cargar datos para consultas
All = pd.read_csv("data/all.csv")
Score = pd.read_parquet('data/score.parquet')
titles_list = All['title'].values

st.write('Sea paciente para la ejecución de las consultas')

# Definir las funciones para las consultas
# Query 1: Duracion maxima
def get_max_duration(year:int, platform:str, duration_type:str): 
    Q1 = All[(All['platform'] == platform) & (All['release_year'] == year) & (All['duration_type'] == duration_type)].sort_values(by = 'duration_int' , ascending=False)
    if len(Q1) > 0:
        # titles_list = Q1['title']   # Observar cuidadosamente que se actualice
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
        Q4_2 = Q4_1.assign(actor=Q4_1.cast.str.split(',')).explode('cast')  # Divide 'cast' por comas
        Q4_3 = Q4_2.cast.value_counts()         # Crea una lista con actores y apariciones.
        max_actor = Q4_3.index[0]               # Obtiene el actor con más apariciones
        max_count = int(Q4_3.iloc[0])           # Obtiene el número de apariciones
        if max_actor == 'nan':                  # Si los valores nulos son los mas frecuentes
            max_actor = Q4_3.index[1]           # Obtiene el segundo actor con más apariciones
            max_count = int(Q4_3.iloc[1])       # Obtiene el número de apariciones correspondiente
        Q4 = dict({'actor': max_actor, 'appearances': max_count})
        return Q4
    else:
        return ({'actor': '', 'appearances': 0})
    
# Query 5: Lista de titulos
def get_titles(year:int, platform:str, duration_type:str):
    Q5 = All[(All['platform'] == platform) & (All['release_year'] == year) & (All['duration_type'] == duration_type)].sort_values(by = 'duration_int' , ascending=False)
    if len(Q5) > 0:
        list_title = Q5['title']
        return list_title
    # else: 
    #     return ("Not titles found with those parameters.")

# Opciones de consulta
options = ['Inicio','Duración máxima', 'Títulos por puntuación', 'Títulos por plataforma', 'Actor con más apariciones','Títulos recomendados']
# query0 = st.sidebar.selectbox('1-Seleccione una consulta', options)
query = st.sidebar.radio('1-Seleccione el tipo de consulta',options)
# usuario_id = st.sidebar.number_input('ID del usuario (Titulos recomendados)', min_value=1, max_value=270895)
# choosed = st.sidebar.selectbox('Seleccione un titulo (Titulos recomendados)', titles_list)
# st.sidebar.button('Recomendar')
progress_text = "Operación en progreso. Espere por favor."
my_bar = st.progress(0, text=progress_text)
for percent_complete in range(100):
    time.sleep(0.05)
    my_bar.progress(percent_complete + 1, text=progress_text)

if query == 'Inicio':
        st.write('Bienvenido a la aplicación de consultas en el catálogo de servicios de streaming')
        st.write('Siga el orden numerico de cada campo para completar su consulta')

# Consulta 1: Duración máxima
if query == 'Duración máxima':
    st.subheader('Duración máxima por año y plataforma')
    year = st.sidebar.number_input('2-Año', min_value=1920, max_value=2023, value=2020, step=1)
    platform = st.sidebar.selectbox('3-Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    duration_type = st.sidebar.selectbox('4-Tipo de duración', ['min', 'season'])
    if st.sidebar.button('Consultar'):
        result = get_max_duration(year, platform, duration_type)
        if isinstance(result, str):
            st.subheader(f'La duración máxima en {duration_type.lower()}s para {year} en {platform} es: {result}.')
        else:
            st.subheader(result)

# Consulta 2: Títulos por puntuación
if query == 'Títulos por puntuación':
    st.subheader('Títulos con una puntuación dada en una plataforma y año determinados')
    platform = st.sidebar.selectbox('2-Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    scored = st.sidebar.number_input('3-Puntuación mínima', min_value=1.0, max_value=5.0, value=3.5, step=0.5)
    year = st.sidebar.number_input('4-Año', min_value=1920, max_value=2023, value=2020, step=1)
    if st.sidebar.button('Consultar'):
        result = get_score_count(platform, scored, year)
        st.subheader(f'Hay {result} títulos en {platform} con una puntuación de {scored} o más en {year}.')

# Consulta 3: Títulos por plataforma
if query == 'Títulos por plataforma':
    st.subheader('Número de títulos en una plataforma dada')
    platform = st.sidebar.selectbox('2-Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    if st.sidebar.button('Consultar'):
        result = get_count_platform(platform)
        st.subheader(f'Hay {result} títulos en {platform}.')



# Consulta 4: Actor con más apariciones
if query == 'Actor con más apariciones':
    st.subheader('Actor con más apariciones por plataforma y año')
    platform = st.sidebar.selectbox('2-Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    year = st.sidebar.number_input('3-Año', min_value=1920, max_value=2022, value=2020, step=1)
    if st.sidebar.button('Consultar'):
        result = get_actor(platform, year)
        if isinstance(result, str):
            st.subheader(result)
        else:
            st.subheader(f'El/los actor/es con más apariciones en {platform} en {year} : {result["actor"].title()}, con {result["appearances"]} apariciones.')

# Consulta 5: Titulos recomendados
if query == 'Títulos recomendados':
    st.subheader('Lista de títulos')
    year = st.sidebar.number_input('2-Año', min_value=1920, max_value=2023, value=2020, step=1)
    platform = st.sidebar.selectbox('3-Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
    duration_type = st.sidebar.selectbox('4-Tipo de duración', ['min', 'season'])
    with st.expander("5-Consultar"):
    # if st.button('Consultar'):
        result = get_titles(year, platform, duration_type)
        choosed = st.selectbox('6-Seleccione un título', result)
        usuario_id = st.number_input('7-ID del usuario (Títulos recomendados)', min_value=1, max_value=270895)
        if st.button('Resultado'):

        
        # Cargar datos para el sistema de recomendacion
            df1 = pd.read_parquet(('data/merge.parquet'))
            df_title = pd.read_csv('data/df_title.csv')

            # Configurar modelo de recomendación
            reader = Reader()
            N_filas = 10000 # Limitamos el dataset a N_filas
            data = Dataset.load_from_df(df1[['userId', 'movieId', 'score']][:N_filas], reader)
                #     
            idx = df_title[df_title['title'] == choosed].index[0]
            movieId = df_title.loc[idx, 'movieId']
            # prediction = model.predict(usuario_id, movieId)
            # Dividir dataset en entrenamiento y prueba
            trainset, testset = train_test_split(data, test_size=.25)
            # Entrenar modelo SVD
            model = SVD()
            model.fit(trainset) 
            predictions = model.test(testset)
            
            
            prediction = model.predict(usuario_id, movieId)
            recomendacion = int(prediction.est * 20)
            # Mostrar la predicción en Streamlit
            st.write('Este título es', recomendacion,'% compatible para el usuario,',usuario_id)
            
            # Agrega un dataframe adicional con las puntuaciones de usuario
            recomendaciones_usuario = df_title[['movieId','title']] # Todos los titulos
            # Debemos extraer las películas que ya ha visto
            usuario_vistas = df1[df1['userId'] == usuario_id] # Filtro por peliculas que el usuario califico
            recomendaciones_usuario.drop(usuario_vistas.movieId, inplace = True,  errors='ignore') # Elimina las peliculas vistas
            recomendaciones_usuario['Estimate_Score'] = recomendaciones_usuario['movieId'].apply(lambda x: model.predict(usuario_id, x).est)
            recomendaciones_usuario = recomendaciones_usuario.sort_values('Estimate_Score', ascending=False)
            st.write('Otros títulos recomendados para el usuario',usuario_id, 'que aun no ha visto.')
            st.dataframe(recomendaciones_usuario)



with st.spinner('Solo un poco mas...'):
    time.sleep(1)
st.success('Listo!', icon="✅")
st.balloons()

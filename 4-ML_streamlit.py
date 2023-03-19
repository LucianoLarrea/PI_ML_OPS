import streamlit as st
import numpy as np
import pandas  as pd
import seaborn as sns
sns.set()
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
# Leer datos
df1 = pd.read_parquet(('data/merge.parquet'))
df_title = pd.read_csv('data/df_title.csv')

# Configurar modelo de recomendación
reader = Reader()
N_filas = 100000 # Limitamos el dataset a N_filas
data = Dataset.load_from_df(df1[['userId', 'movieId', 'score']][:N_filas], reader)
trainset, testset = train_test_split(data, test_size=.25)
model = SVD()
model.fit(trainset)

# Crear interfaz de usuario
st.title('Sistema de recomendación de películas')
st.write('Ingrese el ID del usuario y el puntaje mínimo para las películas recomendadas.')
usuario_id = st.number_input('ID del usuario', min_value=1)
puntaje_minimo = st.slider('Puntaje mínimo para las películas recomendadas', 0.0, 5.0, 4.0, 0.5)

# Realizar recomendación
usuario_vistas = df1[df1['userId'] == usuario_id] # Filtro por peliculas que el usuario califico
recomendaciones_usuario = df_title.copy()
recomendaciones_usuario.drop(usuario_vistas.movieId, inplace=True, errors='ignore')
recomendaciones_usuario = recomendaciones_usuario.reset_index()

if recomendaciones_usuario.shape[0] == 0:
    st.write('Lo sentimos, no hay suficientes películas para hacer una recomendación.')
else:
    recomendaciones_usuario['Estimate_Score'] = recomendaciones_usuario['movieId'].apply(lambda x: model.predict(usuario_id, x).est)
    recomendaciones_usuario = recomendaciones_usuario[recomendaciones_usuario['Estimate_Score'] >= puntaje_minimo]
    recomendaciones_usuario = recomendaciones_usuario.sort_values('Estimate_Score', ascending=False)
    st.write('Las películas recomendadas para el usuario son:')
    st.write(recomendaciones_usuario[['title', 'genres', 'Estimate_Score']].head(10))

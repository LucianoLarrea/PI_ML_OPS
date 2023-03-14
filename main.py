import pandas as pd
from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional

app = FastAPI()

# class Libro(BaseModel):
#     year : Optional[int]
#     platform : Optional[str]
#     duration_type : Optional[str]

# @app.get('/')
# def index():
#     return {'Hola' : 'Mundo'}

@ app.get('/max_duration/{year}/{platform}/{duration_type}')
def get_max_duration(year:int,platform:str,duration_type:str): 
    All = pd.read_csv("data/all.csv")
    # Aplicar filtros opcionales
    if year is not None:
        All = All.loc[All['release_year'] == year]
    if platform is not None:
        All = All.loc[All['platform'] == platform]
    if duration_type is not None:
        All = All.loc[All['duration_type'] == duration_type]

    # Encontrar la película con mayor duración
    max_duration = All['duration_int'].max()
    max_duration_movie = All.loc[All['duration_int'] == max_duration, 'title']
    if len(max_duration_movie) > 0:
        max_duration_movie = max_duration_movie.iloc[0]
    else:
        max_duration_movie = "No movies found with maximum duration"

    # Devolver el resultado
    print(max_duration_movie)
    return max_duration_movie

# year = 2020
# platform = 'amazon'
# duration_type = 'season'
# get_max_duration(year,platform,duration_type)

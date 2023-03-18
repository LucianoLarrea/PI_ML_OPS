# uvicorn main:app --reload

import numpy as np
import pandas as pd
from fastapi import FastAPI
# import asyncio

app = FastAPI()

@app.get('/')
async def index():
    return {'Hola' : 'Mundo'}

# Fucion Query 1
@app.get('/max_duration/{year}/{platform}/{duration_type}')
async def get_max_duration(year:int, platform:str, duration_type:str): 
    All = pd.read_csv("data/all.csv")
    Q1 = All[(All['platform'] == platform) & (All['release_year'] == year) & (All['duration_type'] == duration_type)].sort_values(by = 'duration_int' , ascending=False)
    max_duration_title = Q1['title'].values[0]
    return max_duration_title

# get_max_duration(year, platform, duration_type)
    
# Funcion Query 2
@app.get('/score_count/{platform}/{scored}/{year}')
async def get_score_count(platform:str, scored:int, year:int):
    All = pd.read_csv("data/all.csv")
    Score = pd.read_parquet('data/score.parquet')
    result = Score[(Score['platform'] == platform) & (Score['score'] >= scored) & (All['release_year'] == year)].shape[0]
    return result

# Fucnion Query 3
@app.get('/count_platform/{platform}')
async def get_count_platform(platform:str):
    All = pd.read_csv("data/all.csv")
    All = All.loc[All['platform'] == platform]
    movies_platform = len(All.index)
    return movies_platform

# get_count_platform('amazon')

# Funcion Query 4
@app.get('/get_actor/{platform}/{year}')
async def get_actor(platform:str, year:int):
    All = pd.read_csv("data/all.csv")
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
    
# get_actor('disney', 2020)
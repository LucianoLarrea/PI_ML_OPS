import numpy as np
import pandas as pd
from fastapi import FastAPI
import asyncio

app = FastAPI(title='PI1',
            description='DTS-08')

@app.get('/')
async def index():
    return {'Hola' : 'Mundo'}

@app.get('/max_duration/{year}/{platform}/{duration_type}')
async def get_max_duration(year:int, platform:str, duration_type:str): 
    All = pd.read_csv("data/all.csv")
    Q1 = All[(All['platform'] == platform) & (All['release_year'] == year) & (All['duration_type'] == duration_type)].sort_values(by = 'duration_int' , ascending=False)
    max_duration_title = Q1['title'].values[0]
    return max_duration_title
# get_max_duration(year, platform, duration_type)

async def main():
    max_duration_title = await get_max_duration(2014, 'amazon', 'min')
    print(max_duration_title)

asyncio.run(main())

    # # Encontrar la película con mayor duración
    # max_duration = All['duration_int'].max()
    # max_duration_movie = All.loc[All['duration_int'] == max_duration, 'title']
    # if len(max_duration_movie) > 0:
    #     max_duration_movie = max_duration_movie.iloc[0]
    # else:
    #     max_duration_movie = "No movies found with maximum duration"

    # # Devolver el resultado
    # # print(max_duration_movie)
    # return max_duration_movie
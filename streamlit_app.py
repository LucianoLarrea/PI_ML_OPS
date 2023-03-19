import numpy as np
import pandas as pd
from fastapi import FastAPI
# import asyncio

app = FastAPI()

@app.get('/')
async def index():
    return {'Hola' : 'Mundo'}
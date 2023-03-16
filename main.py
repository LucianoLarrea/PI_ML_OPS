#Importación de las librerías necesarias.
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get('/')
async def read_root():
    return {'Mi primera API'}
    
@app.on_event('startup')
async def startup():
    global df
    df = pd.read_csv('df.csv') 

#función para que reconozca mi servidor local

@app.get('/')
async def index():
    return {'API realizada por Luciano Larrea'}

@app.get('/about/')
async def about():
    return {'PI1 DTS-08'}

# Devuelve la película o serie con duración máxima de acuerdo a las diferentes plataformas
@app.get('/get_max_duration/({year}, {platform}, {min_o_season})')
async def get_max_duration(anio:int,plataforma:str,min_o_season:str):
    #colocamos dentro de una variable llamada result, el resultado de buscar un año y la plataforma
    result = df[(df['release_year']==anio) & (df['platform']==plataforma)]
    #ahora dentro del if, la función toma en cuenta si se ingresa como parámetro la palabra "min" o "seasons", para ver si se quiere buscar una serie o una película
    if min_o_season == 'min':
    #dentro de a se va guardando en resultado maximo de la columna correspondiente a min, lo cual va llenando una lista para luego devolver la de mayor duración en esa plataforma y en ese año
        a = result['min'].max()
        name = result[result['min']==a] ['title']
        name = name.to_list()
        name = name[0]
    else:
        a = result['seasons'].max()
        #dentro de a se va guardando en resultado maximo de la columna correspondiente a seasons, lo cual va llenando una lista para luego devolver la de mayor duración en esa plataforma y en ese año
        name = result[result['seasons']==a] ['title']
        name = name.to_list()
        name = name[0]
    return name

#función que debe devolver la cantidad de peliculas y tv shows que tienen las diferentes plataformas
@app.get('/get_count_platform/({platform})')
async def get_count_platform(plataforma:str):
    #sumamos las cantidad de películas según la plataforma
    movie =((df['platform']==plataforma) & (df.iloc[:, 1].str.contains('Movie'))).sum()  
    #sumamos la cantidad de series según la plataforma
    tv_show =((df['platform']==plataforma) & (df.iloc[:, 1].str.contains('TV Show'))).sum() 
    return ('Platform: ' + str(plataforma) + ' amount of movies: ' + str(movie) + ' amount of TV Shows: ' +str(tv_show))

#función que debe devolver la cantidad de veces que aparece un género con respecto a alguna plataforma
@app.get('/get_listedin/({genero})')
async def get_listedin(genero:str):
    # se crea una lista llamada plataforma con los elementos únicos de la columna platform
    plataforma = list(df.platform.unique()) 
    #se crea esta lista para ir agregando la cantidad de apariciones de cada actor
    cant_apariciones = list()             
    for elemento in plataforma:    
    #se va ubicando nuestro elemento dentro de la variable df_plataforma
        df_plataforma = df[(df.platform == elemento)] 
        #se crea una columna para los indices de la cantidad de veces que se encuentra el genero buscado 
        df_plataforma['indices'] = df_plataforma.listed_in.str.find(genero) 
        #se adjunta la cantidad de apariciones del género para que se vayan sumando, dentro de la lista cant_apariciones y nos devuelve la de índice 0
        cant_apariciones.append(df_plataforma[df_plataforma.indices != -1].indices.shape[0]) 
    return max(cant_apariciones), plataforma[cant_apariciones.index(max(cant_apariciones))]

@app.get('/get_actor/({plataforma},{anio})')
async def get_actor(platform:str, anio:int):
    result = df[(df['platform']==platform) & (df['release_year']==anio)]
    #se empieza realizando una iteración dentro de la columna cast, donde están los actores. Si lo que encuentra es diferente a "sin dato",
    #es decir que encontró información, va a reemplazar la coma y el espacio, por solo la coma. Para realizar luego una separación entre
    #ellos y empezar a diferenciarlos como valores únicos, ya que por cada dato en cast hay muchos actores. Si no encuentra nada, pasa y 
    #sigue con el próximo
    for i in result['cast']:
        if i != 'Sin dato':
            i=i.replace(', ', ',')
        else:
            pass
    #ahora si se crea una lista para ir guardando los actores como valores únicos, separándolos por la coma.
    lista=[]
    for i in result['cast']:
        if i != 'Sin dato':
            s=i.split(',')
            for j in range(len(s)):             
                if s[j] not in lista:
                    lista.append(s[j])
                else:
                    pass
        else:
            pass
    lista=list(set(lista))
    #iniciamos un contador en 0, y creamos un diccionario para ir guardando la cantidad de veces que se repite cada actor
    contador = 0
    dict={}
    for i in lista:
        contador = 0
        for j in result['cast']:
            if i in j.split(','):
                contador+=1
        dict[i]=contador
    return max(dict,key=dict.get)
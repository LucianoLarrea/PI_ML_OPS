# "Sistema de recomendación de películas"
Este repositorio contiene una solución completa para un proyecto de sistema de recomendación para una startup de agregación de plataformas de streaming. El proyecto ha sido resuelto por un equipo que incluye un Data Scientist y un Data Engineer.

## Contexto
La startup provee servicios de agregación de plataformas de streaming y necesita un sistema de recomendación para mejorar la experiencia del usuario. El Data Scientist ha entrenado un modelo de recomendación con buenos resultados, pero los datos presentan problemas de calidad y madurez, lo que impide el uso del modelo en producción.

## Propuesta de trabajo
El proyecto sigue un enfoque iterativo basado en el ciclo de vida de los proyectos de Machine Learning. El objetivo es proporcionar un MVP en una semana. Para ello, se plantea la siguiente propuesta de trabajo:

## Transformaciones de datos
Se deben realizar las siguientes transformaciones de datos:

Generar campo id: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = as123)
Los valores nulos del campo rating deberán reemplazarse por el string “G” (corresponde al maturity rating: “general for all audiences”
De haber fechas, deberán tener el formato AAAA-mm-dd
Los campos de texto deberán estar en minúsculas, sin excepciones
El campo duration debe convertirse en dos campos: duration_int y duration_type. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)
Desarrollo de la API
Se propone el uso del framework FastAPI para disponibilizar los datos de la empresa. Se han definido las siguientes consultas:

Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (la función debe llamarse get_max_duration(year, platform, duration_type))
Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año (la función debe llamarse get_score_count(platform, scored, year))
Cantidad de películas por plataforma con filtro de PLATAFORMA. (La función debe llamarse get_count_platform(platform))
Actor que más se repite según plataforma y año. (La función debe llamarse get_actor(platform, year))
Deployment
Se ha optado por Deta para hacer el deployment de la aplicación, debido a su facilidad de uso y el hecho de que no necesita dockerización.

## Análisis exploratorio de datos
Se debe realizar un análisis exploratorio de datos para investigar las relaciones entre las variables de los datasets, detectar outliers o anomalías y explorar patrones interesantes. Se pueden usar herramientas como pandas profiling, sweetviz, autoviz, entre otros.

## Sistema de recomendación
Una vez que los datos están limpios y disponibles a través de la API, y se ha realizado el análisis exploratorio, se debe entrenar un modelo de machine learning para armar un sistema de recomendación de películas para usuarios. El modelo debe ser capaz de recomendar películas a un usuario dado su ID y una película. Si es posible, se debe desplegar el modelo para tener una interfaz gráfica.

## Estructura del repositorio
En el repositorio se encontrarán los siguientes archivos y carpetas:

README.md: Este archivo que contiene la descripción del proyecto, sus objetivos, y los pasos necesarios para reproducirlo.

LICENSE: Este archivo contiene la licencia bajo la cual se distribuye el proyecto.

requirements.txt: Este archivo contiene una lista de todas las dependencias necesarias para ejecutar el proyecto.

Data: Esta carpeta contiene los datasets en formato CSV utilizados en el proyecto.

EDA: Esta carpeta contiene un Jupyter Notebook con el análisis exploratorio de los datos realizado.

ML: Esta carpeta contiene un Jupyter Notebook con el entrenamiento del modelo de machine learning para el sistema de recomendación.

API: Esta carpeta contiene el código necesario para el desarrollo de la API en FastAPI.

tests: Esta carpeta contiene los archivos necesarios para realizar pruebas unitarias al código de la API.

docs: Esta carpeta contiene la documentación de la API generada automáticamente por Swagger UI.

utils: Esta carpeta contiene algunos scripts auxiliares utilizados en el proyecto.

src: Esta carpeta contiene el código principal del proyecto, incluyendo las transformaciones de los datos y las funciones para la consulta a la API.

deta.yaml: Este archivo contiene la configuración necesaria para realizar el deployment de la API en Deta.

En general, la estructura del repositorio sigue una organización lógica de los diferentes componentes del proyecto, con una carpeta para cada uno de ellos, y una separación clara entre los archivos de datos, el código fuente, la documentación y las pruebas. Además, se incluyen los archivos necesarios para el deployment de la API en Deta.
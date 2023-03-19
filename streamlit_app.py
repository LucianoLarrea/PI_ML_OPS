import streamlit as st
import pandas as pd
import numpy as np

# Crear un título para la aplicación
st.title('Mi primera aplicación de Streamlit')

# Crear un dataframe
df = pd.DataFrame({
  'nombre': ['Juan', 'Ana', 'Pedro', 'Sofía'],
  'edad': [25, 30, 18, 40]
})

# Mostrar el dataframe en una tabla
st.write('Este es mi dataframe:')
st.write(df)

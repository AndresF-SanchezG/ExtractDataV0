import pandas as pd
from datetime import datetime

# Tu DataFrame
dataFrameHoteles = pd.read_excel('./Libro1.xlsx')

# Convertir las columnas de fechas
dataFrameHoteles['Desde'] = pd.to_datetime(dataFrameHoteles['Desde'])
dataFrameHoteles['Hasta*'] = pd.to_datetime(dataFrameHoteles['Hasta*'])

# Definir la fechaDesde
fecha_desde = datetime.strptime('2024-01-03', '%Y-%m-%d')
fecha_hasta = datetime.strptime('2024-01-15', '%Y-%m-%d')

# Filtrar por Hotel y fechas
filtro = (dataFrameHoteles['Hotel'] == 'Barú') & (dataFrameHoteles['Desde'] <= fecha_hasta) & (dataFrameHoteles['Hasta*'] >= fecha_desde)
df_filtrado = dataFrameHoteles[filtro]

# Imprimir solo el contenido del DataFrame filtrado
print('Contenido del DataFrame filtrado:')
print(df_filtrado)








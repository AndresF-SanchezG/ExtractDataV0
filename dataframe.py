import pandas as pd
from datetime import datetime

# Tu DataFrame
dataFrameHoteles = pd.read_excel('./Libro1.xlsx')

# Convertir las columnas de fechas
dataFrameHoteles['Desde'] = pd.to_datetime(dataFrameHoteles['Desde'])
dataFrameHoteles['Hasta*'] = pd.to_datetime(dataFrameHoteles['Hasta*'])

# Definir la fechaDesde
fecha_desde = datetime.strptime('2023-12-19', '%Y-%m-%d')
fecha_hasta = datetime.strptime('2023-12-30', '%Y-%m-%d')

# Filtrar por Hotel y fechas
filtro = (dataFrameHoteles['Hotel'] == 'Maryland') & (dataFrameHoteles['Desde'] <= fecha_hasta) & (dataFrameHoteles['Hasta*'] >= fecha_desde)
df_filtrado = dataFrameHoteles[filtro].copy()  # Agregar .copy() para evitar el SettingWithCopyWarning

# Calcular la nueva columna cant/dias utilizando .apply
df_filtrado['cant_dias'] = df_filtrado.apply(lambda row: (min(row['Hasta*'], fecha_hasta) - max(row['Desde'], fecha_desde)).days + 1, axis=1)

# Identificar la última fila de cada grupo de habitaciones y restar 1 solo a esa fila
last_rows = df_filtrado.duplicated(subset='Habitación', keep='last')
print(last_rows)
df_filtrado.loc[df_filtrado.index.isin(last_rows[last_rows == False].index), 'cant_dias'] -= 1

# Imprimir el contenido del DataFrame filtrado con la nueva columna
print('Contenido del DataFrame filtrado con la nueva columna:')
print(df_filtrado[['Hotel', 'Habitación', 'Desde', 'Hasta*', 'Descuento', 'Sencilla', 'Doble/Adicional', 'Niño', 'cant_dias']])












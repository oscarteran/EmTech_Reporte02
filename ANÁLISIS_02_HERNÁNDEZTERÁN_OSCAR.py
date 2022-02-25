# Importamos las librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargamos los datos
df = pd.read_csv('synergy_logistics_database.csv')
df.head(10)


# 1. Rutas de importación y exportación
# 2. Medio de trasnporte
# 3. Valor de importación y exportación
# 
# - 10 rutas más demandadas
# - 3 medios de trasnporte más importante
# - Países con 80% del valor



# Creación de rutas
routes = [origin + '-' + destiny for origin, destiny in zip(df['origin'], df['destination'])]
df['Routes'] = routes
df.head()


# Recuperamos los nombres únicos de las rutas
names_routes = df['Routes'].unique()


# Agregamos una columna al DF con valores 1 para contar 
df['Total_Use'] = 1


# In[7]:


# Creamos un nuevo DF ordenado por ventas de cada ruta
count_routes = df.groupby('Routes').sum()
count_routes = count_routes.drop(columns=['register_id', 'year'])
count_routes = count_routes.sort_values('Total_Use', ascending=False)


# 10 rutas más demandadas
count_routes.head(10)


count_routes_sales = count_routes.sort_values('total_value', ascending=False)
count_routes_sales.head(10)


# Porcentaje de las 10 rutas con más ventas
total  = count_routes['total_value'].sum()
top_10 = (count_routes['total_value'][:10].sum() / total) * 100
rest   = (count_routes['total_value'][10:].sum() / total) * 100 

print(' ----------------------------------------\n',
      '----Porcentaje de ventas por rutas------\n\n',
      'Top 10:            ', top_10, '\n',  
      'Resto de rutas:    ', rest)



# Recuperamos los nombres únicos de los transportes
names_transport = df['transport_mode'].unique()


count_transport = df.groupby('transport_mode').sum()
count_transport = count_transport.drop(columns=['register_id', 'year'])
count_transport = count_transport.sort_values('Total_Use', ascending=False)


count_transport


df.head()


values = df.groupby(['destination']).sum()
values = values.drop(columns=['register_id', 'year'])
values = values.sort_values('total_value', ascending=False)
values.head(10)


total_value = values['total_value'].sum()
percent_80 = []
contries = []
for i in range(len(values)):
    percent_80.append(values['total_value'][i])
    contries.append(values.index[i])
    if sum(percent_80) >= 0.8*total_value:
        break


print(' ----------------------------------------\n',
      '------Países con el 80% del valor--------\n\n',
      'Total del valor:          $', total_value, '\n')
for i in range(len(contries)):
    print(' País:  ', values.index[i],'\n',
          'Valor:  $', values['total_value'][i] ,'\n')
print(' Valor total de los países:  $', sum(percent_80), '\n',
      'Porcentaje:              :  %', (sum(percent_80)/total_value)*100)


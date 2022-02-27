#!/usr/bin/env python
# coding: utf-8

# In[100]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('bmh')


# In[3]:


df = pd.read_csv('synergy_logistics_database.csv')
df.head(10)


# 1. Rutas de importación y exportación
# 2. Medio de trasnporte
# 3. Valor de importación y exportación
# 
# - 10 rutas más demandadas
# - 3 medios de trasnporte más importante
# - Países con 80% del valor

# ### Rutas

# In[5]:


# Primero vamos a separar en dos DataFrames para contemplar tanto importaciones como exportaciones
df_imports = df[df['direction'] == 'Imports']
df_exports = df[df['direction'] == 'Exports']


# In[60]:


# Creamos una columna auxiliar para contar la demanda
df_imports['Total_Use'] = 1
df_exports['Total_Use'] = 1


# In[9]:


# Creación de rutas
def Routes(df_original):
    df = df_original.copy()
    routes = [origin + '-' + destiny for origin, destiny in zip(df['origin'], df['destination'])]
    df['Routes'] = routes
    df.index = range(0, len(df))
    return df

df_imports = Routes(df_imports)
df_exports = Routes(df_exports)


# In[10]:


df_imports.head()


# In[11]:


df_exports.head()


# In[31]:


def new_df(df_original):
    df = df_original.copy()
    df['Total_Use'] = 1
    df = df.groupby('Routes').sum()
    df = df.drop(columns=['register_id', 'year'])
    df = df.sort_values('total_value', ascending=False)
    return df


# In[32]:


# Creamos un nuevo DF ordenado por ventas de cada ruta
count_routes_imports = new_df(df_imports)


# In[33]:


count_routes_exports = new_df(df_exports)


# In[34]:


# 10 rutas más demandadas
count_routes_imports.head(10)


# In[35]:


# 10 rutas más demandadas
count_routes_exports.head(10)


# In[66]:


def values_routes(df_original):
    df = df_original.copy()
    total = df['total_value'].sum()
    top10 = (df['total_value'][:10].sum() / total) * 100
    rest  = (df['total_value'][10:].sum() / total) * 100 
    return total, top10, rest


# In[38]:


# Porcentaje de las 10 rutas con más ventas
total_imports, top_10_imports, rest_imports = values_routes(count_routes_imports) 


# In[39]:


# Porcentaje de las 10 rutas con más ventas
total_exports, top_10_exports, rest_exports = values_routes(count_routes_exports) 


# In[48]:


print('--------RUTAS MÁS DEMANDADAS POR DIRECCIÓN DE COMERCIO------')
print('     -------------------------------------------------\n',
      '    ----Porcentaje de ventas para importaciones------\n\n',
      '    Top 10:            %', top_10_imports, '\n',  
      '    Resto de rutas:    %', rest_imports)
print()
print('     -------------------------------------------------\n',
      '    ----Porcentaje de ventas para exportaciones------\n\n',
      '    Top 10:            %', top_10_exports, '\n',  
      '    Resto de rutas:    %', rest_exports)
print('-----------------------------------------------------------')


# In[120]:


# 10 rutas más demandadas según dirección
def Plot_Routes(df, direction):
    plt.figure(figsize=(10,6))
    ax = sns.barplot(x=df.index[:10], y=df['total_value'][:10], palette='bone')
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)
    ax.set_title('Top 10 rutas en {}'.format(direction), fontsize=22)
    ax.set_xlabel('Routes', fontsize=16)
    ax.set_ylabel('Total Value [$]', fontsize=16)


# In[121]:


Plot_Routes(count_routes_imports, 'Importación')


# In[122]:


Plot_Routes(count_routes_exports, 'Exportación')


# ### Transporte

# In[61]:


def Transport(df_original):
    df = df_original.copy()
    df = df.groupby('transport_mode').sum()
    df = df.drop(columns=['register_id', 'year'])
    df = df.sort_values('Total_Use', ascending=False)
    return df


# In[64]:


count_transport_imports = Transport(df_imports)
count_transport_imports


# In[65]:


count_transport_exports = Transport(df_exports)
count_transport_exports


# In[136]:


def Plot_Transport(df, direccion):
    plt.figure(figsize=(8,8))
    data = df['total_value']
    labels = df.index
    colors = sns.color_palette('deep')[0:4]
    plt.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
    plt.title('Porcentaje del valor de las {} \n según transporte'.format(direccion), fontsize=18)


# In[137]:


Plot_Transport(count_transport_imports, 'Importaciones')


# In[139]:


Plot_Transport(count_transport_exports, 'Exportaciones')


# ### Valores totales

# In[85]:


def Countries_80(df_original):
    df = df_original.copy()
    df = df.groupby(['destination']).sum()
    df = df.drop(columns=['register_id', 'year'])
    df = df.sort_values('total_value', ascending=False)
    
    total_value = df['total_value'].sum()
    percent_80 = []
    contries = []
    values = []
    for i in range(len(df)):
        values.append(df['total_value'][i])
        contries.append(df.index[i])
        percent_80.append((sum(values)/total_value)*100)
        if sum(percent_80) >= 0.8*total_value:
            break
    data = {'Countries':contries, 'Total_value':values, 'Percent':percent_80}
    df_new = pd.DataFrame(data)
    return df_new


# In[143]:


values_import = Countries_80(df_imports)
values_import.head(10)


# In[166]:


values_export = Countries_80(df_exports)
values_export


# In[170]:


def Plot_80(df, direction, lim, por):
    plt.figure(figsize=(10,6))
    ax = sns.barplot(x=df['Countries'][:lim], y=df['Total_value'][:lim], palette='inferno')
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 60)
    ax.set_title('Países con el {:.2f}$ del valor en {}'.format(por, direction), fontsize=20)
    ax.set_xlabel('Países', fontsize=16)
    ax.set_ylabel('Total Value [$]', fontsize=16)


# In[171]:


Plot_80(values_import, 'Importación', 6, values_import['Percent'][5])


# In[172]:


Plot_80(values_export, 'Exportación', 13, values_export['Percent'][12])


# In[ ]:


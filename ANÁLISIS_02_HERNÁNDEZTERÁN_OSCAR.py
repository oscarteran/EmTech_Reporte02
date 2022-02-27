'''
Autor:
      Oscar Hernández Terán

Instrucciones del programa:
      1. Rutas de importación y exportación.
      2. Medio de transporte utilizado.
      3. Valor total de importaciones y exportaciones.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('bmh')


df = pd.read_csv('synergy_logistics_database.csv')
print('--------------------------------------------------')
print('----- Forma general de la Base de datos (BD) ----- \n\n')
print(df.head(10))
print('\n\n')


# Primero vamos a separar en dos DataFrames para contemplar tanto importaciones como exportaciones
df_imports = df[df['direction'] == 'Imports']
df_exports = df[df['direction'] == 'Exports']


# Creamos una columna auxiliar para contar la demanda
def Ones(df_original):
      df = df_original.copy()
      df['Total_Use'] = 1
      return df
df_imports = Ones(df_imports)
df_exports = Ones(df_exports)



#--------------------------------------------------------
# ---------------------PUNTO 1---------------------------
#--------------------------------------------------------

# Creación de rutas
def Routes(df_original):
    df = df_original.copy()
    routes = [origin + '-' + destiny for origin, destiny in zip(df['origin'], df['destination'])]
    df['Routes'] = routes
    df.index = range(0, len(df))
    return df

df_imports = Routes(df_imports)
df_exports = Routes(df_exports)



print('--------------------------------------------------')
print('------- Creación de la columna de rutas ---------- \n\n')
print('IMPORTACIONES')
print(df_imports.head())
print('\n\n')
print('EXPORTACIONES')
print(df_exports.head())
print('\n\n')



# Creamos una función para generar un nuevo DF con nueva estructura
def new_df(df_original):
    df = df_original.copy()
    df['Total_Use'] = 1
    df = df.groupby('Routes').sum()
    df = df.drop(columns=['register_id', 'year'])
    df = df.sort_values('total_value', ascending=False)
    return df

# Creamos un nuevo DF ordenado por ventas de cada ruta
count_routes_imports = new_df(df_imports)
count_routes_exports = new_df(df_exports)


# 10 rutas más demandadas
print('--------------------------------------------------')
print('--------------- Top 10 rutas  -------------------- \n\n')
print('IMPORTACIONES')
print(count_routes_imports.head(10))
print('\n\n')
print('EXPORTACIONES')
print(count_routes_exports.head(10))
print('\n\n')


# Función para devolver valores porcentuales
def values_routes(df_original):
    df = df_original.copy()
    total = df['total_value'].sum()
    top10 = (df['total_value'][:10].sum() / total) * 100
    rest  = (df['total_value'][10:].sum() / total) * 100 
    return total, top10, rest

# Porcentaje de las 10 rutas con más ventas
total_imports, top_10_imports, rest_imports = values_routes(count_routes_imports) 
total_exports, top_10_exports, rest_exports = values_routes(count_routes_exports) 


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
print('\n\n')


# 10 rutas más demandadas según dirección. Gráfico.
def Plot_Routes(df, direction):
    plt.figure(figsize=(9,6))
    ax = sns.barplot(x=df.index[:10], y=df['total_value'][:10], palette='bone')
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 70)
    ax.set_title('Top 10 rutas en {}'.format(direction), fontsize=22)
    ax.set_xlabel('Routes', fontsize=16)
    ax.set_ylabel('Total Value [$]', fontsize=16)
    plt.show()


# Llamado a la función
Plot_Routes(count_routes_imports, 'Importación')
Plot_Routes(count_routes_exports, 'Exportación')





#--------------------------------------------------------
# ---------------------PUNTO 2---------------------------
#--------------------------------------------------------

# Creamos una función para observar los medios de transporte
def Transport(df_original):
    df = df_original.copy()
    df = df.groupby('transport_mode').sum()
    df = df.drop(columns=['register_id', 'year'])
    df = df.sort_values('Total_Use', ascending=False)
    return df


# Llamado a la función
count_transport_imports = Transport(df_imports)
count_transport_exports = Transport(df_exports)


print('--------------------------------------------------')
print('---------------- Trasnportes --------------------- \n\n')
print('IMPORTACIONES')
print(count_transport_imports)
print('\n\n')
print('EXPORTACIONES')
print(count_transport_exports)
print('\n\n')


# Gráfico para observar la contribución de cada medio de transporte
def Plot_Transport(df, direccion):
    plt.figure(figsize=(8,8))
    data = df['total_value']
    labels = df.index
    colors = sns.color_palette('deep')[0:4]
    plt.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
    plt.title('Porcentaje del valor de las {} \n según transporte'.format(direccion), fontsize=18)
    plt.show()



# Llamado a la función
Plot_Transport(count_transport_imports, 'Importaciones')
Plot_Transport(count_transport_exports, 'Exportaciones')





#--------------------------------------------------------
# ---------------------PUNTO 3---------------------------
#--------------------------------------------------------

# Función para asignar a cada país su total y porcentaje acumulado ordenado
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


# Llamado a la función
values_import = Countries_80(df_imports)
values_export = Countries_80(df_exports)



print('--------------------------------------------------')
print('------- Paises con aportación del 80% ------------ \n\n')
print('IMPORTACIONES')
print(values_import)
print('\n\n')
print('EXPORTACIONES')
print(values_export)
print('\n\n')


# Función para generar gráfico de los países que en conjunto representan el 80%
def Plot_80(df, direction, lim, por):
    plt.figure(figsize=(9,6))
    ax = sns.barplot(x=df['Countries'][:lim], y=df['Total_value'][:lim], palette='inferno')
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 60)
    ax.set_title('Países con el {:.2f}$ del valor en {}'.format(por, direction), fontsize=20)
    ax.set_xlabel('Países', fontsize=16)
    ax.set_ylabel('Total Value [$]', fontsize=16)
    plt.show()


# Llamado a las funciones
Plot_80(values_import, 'Importación', 6, values_import['Percent'][5])
Plot_80(values_export, 'Exportación', 13, values_export['Percent'][12])




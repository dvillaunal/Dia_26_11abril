'''
¿Qué es un DataFrame?:

Un DataFrame de Pandas es una estructura de datos bidimensional,
como una matriz bidimensional o una tabla con filas y columnas.
'''
import pandas as pd
import xlrd

import warnings
import numpy as np

# ejecutar un bloque de código y capturar las advertencias:
with warnings.catch_warnings():
	# ignorar todos los avisos de captura:
	warnings.filterwarnings("ignore")
	# ejecutar código que generará advertencias
print('intente hacer try y except para suprimir el error y no me dio')

modelo = pd.ExcelFile('Modelo_Factura.xls')

'''
Creamos un dataframe donde almacenamos los datos de la Hoja de Calculo
'''
dm = modelo.parse('Hoja1')

'Visualicemos los datos'
print(dm)

'''
Vamos a calcular con este data frame:
-> Bruto (Precio Total sin incluir el iva)
-> Iva (16%)
-> Total
'''

# Volvemos a Articulo el index del dataframe:

sdm_articulo = dm['ARTICULO'].squeeze()
dm = dm.set_index('ARTICULO')

print('Visualizamos el Cambio: ')
print(dm)

# Convertimos el DataFrame a Series:
'con el metodo .squeeze()'
'nos deveuelve una serie data frame selecionado'

sdm_precio = dm['PRECIO'].squeeze()
sdm_cantidad = dm['CANTIDAD'].squeeze()

'Calculamos el Valor Bruto de los productos'
s_bruto = sdm_precio * sdm_cantidad

'Calculamos el IVA (16%) de los productos'
s_Iva = sdm_precio * (0.16)

'Calculamos el Valor TOTAL de los productos'
s_total = s_bruto + s_Iva

# Ahora concatenamos varias series para hacer un dataframe:
'con el metodo .concat() podemos concatenar en este caso una lista de series'
'con el axis=1, le decimos que organice los valores, ya que por defecto truncara uno con otros= una liista infinita'
resultados0 = pd.concat([sdm_precio,sdm_cantidad,s_bruto,s_Iva,s_total], axis=1)

# Ponemos nombre a las columnas del datafram dado:
resultados0.columns = ['PRECIO', 'CANTIDAD','BRUTO','IVA_16%(xU)', 'TOTAL']
resultados0.to_excel('Resultados_Factura.xls')
print(resultados0)

'Con el metodo .describe() podemos generar estadisticas basicas del dataframe selecionado'
'nos calcula, la media, varianza, sd, los percentiles y minimos & maximos'

estaR0 = resultados0.describe()
estaR0.to_excel('Estadisticas_Resultados_Factura.xls')

# Ejercicio 2:
'''
Dada una base de datos de 'Sueldo y Comisiones de vendedores'
Vamos a Cacular:
-> Comisíon por ventas del mes (2% x Venta del Mes)
-> El total del sueldo, (Sueldo base + Comisíones)
  -> Sueldo base == $ 90.000
-> Porcentaje de ventas s/total (VentaxPersona/Total de ventas)
'''

base = pd.ExcelFile('Sueldo_Comision.xls')

'''
Creamos un dataframe donde almacenamos los datos de la Hoja de Calculo
'''

db = base.parse('Hoja1')

'Visualicemos los datos'
print(db)

'Cambiamos el Indice por el nombre de cada vendedor'
db = db.set_index('Vendedor')


# Vovelmos series las columnas del dataframe para hacer operaciones aritmeticas:
sdb_ventas = db['Ventas'].squeeze()
sdb_sueldobase = db['Sueldo Base'].squeeze()

# Calculemos comisíon por ventas del mes:
s_comision = sdb_ventas * (0.02)

# Calculamos total (sueldo base + comision):
'-> Sueldo base == $ 90.000'

sueldo_base = 90000

s_total = sueldo_base + s_comision

# CALCULAMOS % de ventas s/total:
'''
dado un data frame
obtenemos la suma de cada columna usando la función sum()
df['COLUMNA'].sum()

retorna la suma de los elementos de esa columna
'''

suma_ventas = db['Ventas'].sum()

s_por_ventas = sdb_ventas / suma_ventas

# Volvemos la series un dataframe:
resultados1 = pd.concat([sdb_ventas, sdb_sueldobase, s_comision, s_total, s_por_ventas], axis=1)

resultados1.columns = ['VENTAS', 'SUELDO BASE', 'COMISIÓN', 'TOTAL', '% Ventas s/total']

resultados1.to_excel('Resultados2.xls')

'Estadisticas basicas del archivo anterior:'
estaR1 = resultados1.describe()
estaR1.to_excel('Estadisticas_Resultados_Sueldo_Comision.xls')
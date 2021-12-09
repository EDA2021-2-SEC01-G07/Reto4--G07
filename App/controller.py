"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config as cf
import model.catalog as ct

import model.req2 as rq2
import model.req1 as rq1
import model.req3 as rq3
import model.req4 as rq4
import model.req5 as rq5
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = ct.newCatalog()
    return catalog
# Funciones para la carga de datos
def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    airports = cf.data_dir + 'airports-utf8-large.csv'
    airports_file = csv.DictReader(open(airports, encoding='utf-8'))
    first=next(airports_file)
    firstdir=None
    ct.addAirport(catalog,first)
    for airport in airports_file:
        ct.addAirport(catalog, airport)
    
    routes = cf.data_dir + 'routes-utf8-large.csv'
    routes_file = csv.DictReader(open(routes, encoding='utf-8'))    
    for route in routes_file:
        a = ct.addConnections(catalog, route, firstdir)
        if a !=None and firstdir==None:
            firstdir = a
    
    ct.loadStronglyConnected(catalog)

    cities = cf.data_dir + 'worldcities-utf8.csv'
    city_file = csv.DictReader(open(cities, encoding='utf-8'))
    for city in city_file:
        last = city
        ct.addCity(catalog,city)
    return catalog, first, firstdir, last

def req2(catalog, iata1, iata2):
    return rq2.req2(catalog, iata1, iata2)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def findInterconected(catalog):
    return rq1.findInterconected(catalog)

def req3(catalog,origin_city,destiny_city):
    return rq3.shortCityPath(catalog,origin_city,destiny_city)

def req4(catalog, city, miles):
    return rq4.Millas(catalog, city, miles)

def req5(catalog, iata):
    return rq5.closedAirport(catalog,iata)
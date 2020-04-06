from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render, get_object_or_404
import requests

todos_episodios = []
todos_personajes = []
todos_lugares = []

def cargar_contenido():
    todos_episodios = []
    todos_personajes = []
    todos_lugares = []
    cant_episodios = requests.get("https://integracion-rick-morty-api.herokuapp.com/api/episode/")
    cant_episodios = cant_episodios.json()
    cant_personajes = requests.get("https://integracion-rick-morty-api.herokuapp.com/api/character/")
    cant_personajes = cant_personajes.json()
    cant_lugares = requests.get("https://integracion-rick-morty-api.herokuapp.com/api/location/")
    cant_lugares = cant_lugares.json()
    cant_episodios = int(cant_episodios["info"]["pages"])
    cant_personajes = int(cant_personajes["info"]["pages"])
    cant_lugares = int(cant_lugares["info"]["pages"])
  
    
    i=1
    for i in range(1,cant_episodios+1):
            url = f'https://integracion-rick-morty-api.herokuapp.com/api/episode/?page='
            url = url + str(i)
            response = requests.get(url)
            data = response.json()
            data = data["results"]
            for episode in data:
            	nombre = episode["name"]
            	identificador = episode["id"]
            	todos_episodios.append([identificador,nombre])   
            i+=1
  
    j=1
    for j in range(1,cant_personajes+1):
            url = f'https://integracion-rick-morty-api.herokuapp.com/api/character/?page='
            url = url + str(j)
            response = requests.get(url)
            data = response.json()
            data = data["results"]
            for episode in data:
            	nombre = episode["name"]
            	identificador = episode["id"]
            	todos_personajes.append([identificador,nombre])
            j+=1

    k=1
    for k in range(1,cant_lugares+1):
            url = f'https://integracion-rick-morty-api.herokuapp.com/api/location/?page='
            url = url + str(k)
            response = requests.get(url)
            data = response.json()
            data = data["results"]
            for episode in data:
            	nombre = episode["name"]
            	identificador = episode["id"]
            	todos_lugares.append([identificador,nombre])
    
            k+=1
    diccionario = {"todos_episodios": todos_episodios, "todos_personajes": todos_personajes, "todos_lugares": todos_lugares}
    return diccionario


def buscar(request):
    episodios_encontrados=[]
    personajes_encontrados=[]
    lugares_encontrados=[]
   
    query = request.GET.get("query")
    if query:
        resultado = cargar_contenido()
        todos_episodios = resultado["todos_episodios"]
        todos_personajes = resultado["todos_personajes"]
        todos_lugares = resultado["todos_lugares"]
        
        for episodio in todos_episodios:
            if query.lower() in episodio[1].lower():
                episodios_encontrados.append(episodio)

        for personaje in todos_personajes:
            if query.lower() in personaje[1].lower():
                personajes_encontrados.append(personaje)

        for lugar in todos_lugares:
            if query.lower() in lugar[1].lower():   
                lugares_encontrados.append(lugar)
    else:
        query = "no se ingresó nada para buscar"
    
 
    diccionario = {"query": query,"episodios_encontrados":episodios_encontrados, "personajes_encontrados": personajes_encontrados, "lugares_encontrados":lugares_encontrados}
    doc_externo = loader.get_template("plantillaresultados.html")
    documento = doc_externo.render(diccionario)
    return HttpResponse(documento)

def home(request):
    
    response = requests.get("https://integracion-rick-morty-api.herokuapp.com/api/episode/")
    data = response.json()
   
    paginas = int(data["info"]["pages"])   
    diccionario = {"nombre":[],"fecha":[],"codigo":[]}
    i = 1
    for i in range(1, paginas+1):
        url = 'https://integracion-rick-morty-api.herokuapp.com/api/episode/?page='
        url = url + str(i)
        response = requests.get(url)
        data = response.json()
        resultado = data["results"]

        for episode in resultado:
            diccionario["nombre"].append([episode["id"],episode["name"],i])
            diccionario["fecha"].append(episode["air_date"])
            diccionario["codigo"].append(episode["episode"])
        
        i+=1

    doc_externo = loader.get_template("plantillahome.html")
    documento = doc_externo.render(diccionario)
    return HttpResponse(documento)





def episodio(request, identificador):
    url = 'https://integracion-rick-morty-api.herokuapp.com/api/episode/'
    url+= str(identificador)
    response = requests.get(url)
    data = response.json()
    queryset = request.GET.get("buscar")
    if queryset:
        buscar(queryset)
    
    nombre = data["name"]
    fecha = data["air_date"]
    codigo = data["episode"]
    personajes = data["characters"]
    lista_personajes = []
    for personaje in personajes:
        response2 = requests.get(personaje)
        data2 = response2.json()
        lista_personajes.append([data2["id"],data2["name"]])

    diccionario = {"identificador": identificador,"nombre":nombre, "fecha": fecha, "codigo":codigo, "personajes": lista_personajes}
    doc_externo = loader.get_template("plantillaepisodio.html")
    documento = doc_externo.render(diccionario)
    return HttpResponse(documento)
    

def personaje(request, identificador):
    url = "https://integracion-rick-morty-api.herokuapp.com/api/character/"
    url = url + str(identificador)
    
    response = requests.get(url)
    data = response.json() 
    queryset = request.GET.get("buscar")
    if queryset:
        buscar(queryset)
       
    nombre = data["name"]
    estado = data["status"]
    especie = data["species"]
    tipo = data["type"]
    if tipo == "":
        tipo = "No se especifica"
    genero = data["gender"]
    origen = data["origin"]["name"]
    imagen = data["image"]
    lugar = data["location"]["name"]
    url_lugar = data["location"]["url"]
    if url_lugar == "" :
        lugar = 0
        id_lugar = 0
    else:
        response3 = requests.get(url_lugar)
        data3 = response3.json()
        id_lugar = data3["id"]
    episodios = data["episode"]
    lista_episodios = []
    for episodio in episodios:
        response2 = requests.get(episodio)
        data2 = response2.json()
        lista_episodios.append([data2["id"],data2["name"]])

    diccionario = {"nombre":nombre,"imagen":imagen,"lista_episodios":lista_episodios, "lugar":lugar, "id_lugar":id_lugar,"estado":estado, "especie":especie, "tipo":tipo, "genero":genero, "origen":origen}
    doc_externo = loader.get_template("plantillapersonaje.html")
    documento = doc_externo.render(diccionario)
    return HttpResponse(documento)

def lugar(request, id_lugar):
    url ="https://integracion-rick-morty-api.herokuapp.com/api/location/"
    url+= str(id_lugar)
    response = requests.get(url)
    data = response.json()
    queryset = request.GET.get("buscar")
    if queryset:
        buscar(queryset)
        
    nombre = data["name"]
    tipo = data["type"]
    if tipo == "":
        tipo = "No se especifica"
    dimension = data["dimension"]
    residentes = data["residents"]
    lista_residentes = []
    for residente in residentes:
        response2 = requests.get(residente)
        data2 = response2.json()
        lista_residentes.append([data2["id"],data2["name"]])
    diccionario = {"nombre":nombre, "tipo":tipo, "dimension": dimension, "lista_residentes": lista_residentes}
    doc_externo = loader.get_template("plantillalugar.html")
    documento = doc_externo.render(diccionario)
    return HttpResponse(documento)

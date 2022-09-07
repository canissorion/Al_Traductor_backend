from lector import fonemasToRuta, stringToFonema
from traductor_ingesp import translate_ingesp
from traductor import translate
import json
import sys


sys.stdout.reconfigure(encoding='utf-8')

def t_ing_esp(data):
    sentence = str(data["text"])
    try: 
        traduccion = translate_ingesp(sentence)
        return traduccion
    except Exception:
        return "No se ha podido traducir"

def t_esp_map(data):
    sentence = str(data["text"])
    modelo = 'mapespanol.h5'
    dataset = 'mapespanol.csv'
    try:
        traduccion = translate(modelo,dataset, sentence)
        return traduccion
    except Exception:
        return "No se ha podido traducir"

def tts_map(data):
    sentence = str(data["text"])
    sentence = sentence.replace('"', "")
    sentence = sentence.replace('\n', "")
    filename = "data/diccionario_fonemas.json"
    with open(filename) as diccionario_fonemas:
        json_data = json.load(diccionario_fonemas)
    cadena = ""
    rutas = []
    try:
        cadena = stringToFonema(sentence, json_data)
        print(cadena)
        fonemasToRuta(cadena, rutas)
        print(rutas)
        return rutas
    except Exception:
        return "error"
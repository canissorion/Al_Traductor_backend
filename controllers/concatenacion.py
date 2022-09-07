# -*- coding: utf-8 -*-
'''
@desc: 
@author: Facundo Alexandre B. (facundo.alexandreb@utem.cl)
@created_at: 13/06/2022 14:44PM

Cualquier duda sobre el código, favor contactar al mail.
'''

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("data/diccionario_fonemas.json") as diccionario_fonemas:
        json_data = json.load(diccionario_fonemas)

def get_cadena_pronunciable(cadena_original):
    cadena_pronunciable = cadena_original

    # Recorriendo letras del string recibido, una por una
    for index, letra in enumerate(cadena_pronunciable):
        hay_siguiente_letra = index + 1 < len(cadena_pronunciable) 
        siguiente_letra = cadena_pronunciable[index+1] if hay_siguiente_letra else None

        # Primero, se verifican casos especiales ('ch', 'tr', 'ng')
        if (letra == "c" and siguiente_letra == "h"):
            cadena_pronunciable = re.sub('ch', json_data['ch']['pronunciacion'], cadena_pronunciable)
        elif (letra == 't' and siguiente_letra == 'r'):
            cadena_pronunciable = re.sub('tr', json_data['tr']['pronunciacion'], cadena_pronunciable)
        elif (letra == 'n' and siguiente_letra == 'g'):
            cadena_pronunciable = re.sub('ng', json_data['ng']['pronunciacion'], cadena_pronunciable)
        else:
            # Cualquier otra letra individual (fuera de casos especiales)

            if (letra in json_data.keys()):
                # Si la letra está en el diccionario
                cadena_pronunciable = re.sub(letra, json_data[letra]['pronunciacion'], cadena_pronunciable)

             # Si la letra no está en el diccionario, se deja como viene, es decir, no se reemplaza.
    return cadena_pronunciable


cadena_pronunciable = get_cadena_pronunciable("llichntallulng")
#print(cadena_pronunciable)
from traductor import translate
from traductor_ingesp import translate_ingesp

modelo = 'backend/modelo20k-150-iteraciones.h5'
dataset = 'backend/mapespanol - reducido - 20k.csv'
traduccion = translate(modelo,dataset,'buenas tardes')

#print(traduccion)

#traduccion2 = translate_ingesp ('good morning')

#print(traduccion2)

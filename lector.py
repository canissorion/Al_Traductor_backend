
def diccRutas(array, letra):
	dicc = {
		"e": "assets/audios/e.wav",
		"i": "assets/audios/i.wav",
		"a": "assets/audios/a.wav",
		"o": "assets/audios/o.wav",
		"u": "assets/audios/u.wav",
		"": "assets/audios/u2.wav",
		"t": "assets/audios/ch.wav",
		"θ": "assets/audios/d.wav",
		"f": "assets/audios/f.wav",
		"g": "assets/audios/g.wav",
		"k": "assets/audios/k.wav",
		"l": "assets/audios/l.wav",
        "l": "assets/audios/l2.wav",        
		"ʎ": "assets/audios/Ll.wav",
		"m": "assets/audios/m.wav",
		"n": "assets/audios/n.wav",
		"": "assets/audios/ng.wav",
		"": "assets/audios/enhe.wav",
		"p": "assets/audios/p.wav",
		"": "assets/audios/r.wav",
		"s": "assets/audios/s.wav",
		"t": "assets/audios/t.wav",
		"": "assets/audios/tr.wav",
		"w": "assets/audios/w.wav",
		"j": "assets/audios/y.wav",
		" ": "assets/audios/silencio.wav",
	}
	array.append(dicc[letra])


def stringToFonema(string, json_data):
    i = 0
    largo = len(string)
    cadena = ""
    while(i<largo):
        aux = True
        if(i<largo-1):
            if(string[i] == "c" and string[i+1] == "h"):
                temp = string[i]
                i+=1
                temp = temp + string[i]
                aux = False
            if(aux and string[i] == "t" and string[i+1] == "r"):
                temp = string[i]
                i+=1
                temp = temp + string[i]
                aux = False
            if(aux and string[i] == "l" and string[i+1] == "l"):
                temp = string[i]
                i+=1
                temp = temp + string[i]
                aux = False
            if(aux and string[i] == "n" and string[i+1] == "g"):
                temp = string[i]
                i+=1
                temp = temp + string[i]
                aux = False
        if(aux):
            temp = string[i]
        cadena += (json_data[temp]["fonema"])
        i+=1
    return cadena


def fonemasToRuta(cadena, rutas):
    i=0
    largo = len(cadena)
    while(i<largo):
        aux = True
        if(i<largo-1):
            if(cadena[i] == "t" and cadena[i+1] == ""):
                temp = cadena[i]
                i+=1
                temp = temp + cadena[i]
                aux = False
            if(aux and cadena[i] == "" and cadena[i+1] == ""):
                temp = cadena[i]
                i+=1
                temp = temp + cadena[i]
                aux = False
        if(aux):
            temp = cadena[i]
        i+=1
        diccRutas(rutas,temp)

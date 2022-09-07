import numpy as np
from keras_transformer import get_model, decode
import pandas as pd
np.random.seed(0)

# Función que construye diccionario para un idioma, recibe un
# arreglo de tokens, devuleve un diccionario
def build_token_dict(token_list):
	token_dict = {
		'<PAD>': 0,
		'<START>': 1,
		'<END>': 2
	}
	for tokens in token_list:
		for token in tokens:
			if (token not in token_dict):
				token_dict[token] = len(token_dict)
	return token_dict

def build_token_dict_inv(token_dict):
	token_dict_inv = {}
	for k,v in token_dict.items():
		token_dict_inv[v] = k
	return token_dict_inv

###################

def datos(x):
	dataset = pd.read_csv(x,sep=';')
	dataset = dataset.to_numpy().tolist()
	source_token = []
	target_token = []
	#print(dataset)

	for sentence in dataset:
		target_token.append(str(sentence[0]).split())
		source_token.append(str(sentence[1]).split())
		
	
	#creaccion de diccionarios
	source_token_dict = build_token_dict(source_token)
	target_token_dict = build_token_dict(target_token)

	#dict invertido de target
	target_token_dict_inv = build_token_dict_inv(target_token_dict) 

	#Agrega start, end y pad a las frases de entrenamiento
	encoder_tokens = [['<START>'] + tokens + ['<END>'] for tokens in source_token]
	decoder_tokens = [['<START>'] + tokens + ['<END>'] for tokens in target_token]
	output_tokens = [tokens + ['<END>'] for tokens in source_token]

	source_max_len = max(map(len, encoder_tokens))
	target_max_len = max(map(len, decoder_tokens))
	encoder_tokens = [tokens + ['<PAD>'] *(source_max_len-len(tokens)) for tokens in encoder_tokens]
	decoder_tokens = [tokens + ['<PAD>'] *(target_max_len-len(tokens)) for tokens in decoder_tokens]
	output_tokens = [tokens + ['<PAD>'] *(target_max_len-len(tokens)) for tokens in output_tokens]

	# print(encoder_tokens[120000])


	# encoder_input = [list(map(lambda x: source_token_dict[x], tokens))
	#                 for tokens in encoder_tokens]
	# decoder_input = [list(map(lambda x: target_token_dict[x], tokens))
	#                 for tokens in decoder_tokens]
	# output_decoded = [list(map(lambda x: [target_token_dict[x]], tokens))
	#                 for tokens in output_tokens]
	


	#crear red transformer, entrenar y guardar modelo

	token = max(len(source_token_dict),len(target_token_dict))
	#model.summary()

	# entrenamiento
	# x = [np.array(encoder_input), np.array(decoder_input)]
	# y = np.array(output_decoded)
	# model.fit(x,y, epochs=25, batch_size=32)
		
	# Guardar el Modelo
	# model.save('modeloentrenado.h5') 


	return source_token_dict, target_token_dict, target_token_dict_inv, token


def translate(modelo, dataset, sentence):
	source_token_dict, target_token_dict, target_token_dict_inv, numero = datos(dataset)
	#cargar modelo
	model = get_model(
    token_num = numero,
    embed_dim = 32,
    encoder_num = 2,
    decoder_num = 2,
    head_num = 4,
    hidden_dim = 128,
    dropout_rate = 0.05,
    use_same_embed= False,
	)
	model.compile('adam', 'sparse_categorical_crossentropy', metrics=['accuracy'])
	
	model.load_weights(modelo)

	sentence_tokens = [tokens + ['<END>','<PAD>'] for tokens in [sentence.split(' ')]]
	tr_input = [list(map(lambda x: source_token_dict[x], tokens))
				for tokens in sentence_tokens][0]
	decoded=decode(
		model,
		tr_input,
		start_token = target_token_dict['<START>'],
		end_token = target_token_dict['<END>'],
		pad_token = target_token_dict['<PAD>']
	)

	print("Frase original: {}".format(sentence))
	print("Traducción: {}".format(' '.join(map(lambda x: target_token_dict_inv[x], decoded[1:-1]))))
	return '{}'.format(' '.join(map(lambda x: target_token_dict_inv[x], decoded[1:-1])))


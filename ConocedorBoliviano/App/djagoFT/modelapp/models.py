from django.db import models

# Create your models here.
import keras
import keras_transformer

from keras_layer_normalization import LayerNormalization
from keras_multi_head import MultiHeadAttention
from keras_position_wise_feed_forward import FeedForward
from keras_pos_embd import TrigPosEmbedding
from keras_embed_sim import EmbeddingRet, EmbeddingSim
def get_custom_objects():
    return {
        #'gelu': gelu,
        'LayerNormalization': LayerNormalization,
        'MultiHeadAttention': MultiHeadAttention,
        'FeedForward': FeedForward,
        'TrigPosEmbedding': TrigPosEmbedding,
        'EmbeddingRet': EmbeddingRet,
        'EmbeddingSim': EmbeddingSim,
    }

from keras.models import load_model
model = load_model('models/completeModel.h5', custom_objects=get_custom_objects())  
import numpy as np
from keras_transformer import get_model, decode
np.random.seed(0) #Semilla
import json
with open('models/answersCOMPLETE.json', encoding='utf-8') as file:
    data = json.load(file)#acceder a la raiz del json
data_respuestas = data["answers"]
#print(data_respuestas[0])
#respuestas
respuestas = data_respuestas[0]["answer"]
#print("\nanswer access => ",respuestas)
#Preguntas
pregunta = data_respuestas[0]["Question"]
#print("\npregunta access => ",pregunta)
#Long datos
#print("cantidad de respuestas en el dataset : ", len(data_respuestas))
data_resp = []
respuestas = []
preguntas = []
for data in data_respuestas:
  preguntas.append(data["Question"])
  respuestas.append(data["answer"])
data_resp.append(preguntas)
data_resp.append(respuestas)
pregunta_tokens = []
for sentence in preguntas:
  pregunta_tokens.append(sentence.split(' '))

#print(pregunta_tokens[0])

respuesta_tokens = []
for sentence in respuestas:
  respuesta_tokens.append(sentence.split(' '))

#print(respuesta_tokens[1])
def build_token_dict(token_list):
  token_dict = {
      '<PAD>': 0,
      '<START>': 1,
      '<END>': 2
  }

  # Se lee los tokens
  for tokens in token_list:
    for token in tokens:
      if token not in token_dict:
        token_dict[token] = len(token_dict)
  
  return token_dict

# tokens preguntas
pregunta_token_dict = build_token_dict(pregunta_tokens)

# tokens respuesta
respuesta_token_dict = build_token_dict(respuesta_tokens)

# Invertimos el diccionario
respuesta_token_dict_inv = {v:k for k,v in respuesta_token_dict.items()}
def AnswersGenerator(sentences):
  sentence_tokens = [tokens + ['<END>', '<PAD>'] for tokens in [sentences.split(' ')]]
  print(sentence_tokens)
  tr_input = [list(map(lambda x: pregunta_token_dict[x], tokens)) for tokens in sentence_tokens][0]
  print(tr_input)
  decoded = decode(
      model,
      tr_input,
      start_token = respuesta_token_dict['<START>'],   
      end_token = respuesta_token_dict['<END>'],   
      pad_token = respuesta_token_dict['<PAD>']   
  )
  resp = format(' '.join(map(lambda x: respuesta_token_dict_inv[x], decoded[1:-1])))
  #aqui imprimimos los resultados
  #print("Pregunta : {} ".format(sentences))
  print("Respuesta :", resp)
  return resp
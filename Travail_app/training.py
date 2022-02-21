import random
import json
import pickle
import numpy as numpy
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


lemmatizer= WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = []
classes = []
doc = []
charactere = ['?','!','.','...',',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        wrd_list=nltk.word_tokenize(pattern)
        words.extend(wrd_list)
        doc.append((wrd_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in charactere]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(words, open('classes.pkl', 'wb'))

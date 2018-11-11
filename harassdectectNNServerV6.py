# use natural language toolkit
import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
import sys
from flask import Flask, request, redirect
from flask import make_response
from flask import jsonify
from flask_cors import CORS
import requests
import io
import hashlib


stemmer = LancasterStemmer()

training_data = []
training_data.append({"class":"generic", "sentence":"how are you?"})
training_data.append({"class":"generic", "sentence":"how is your day?"})
training_data.append({"class":"generic", "sentence":"good day"})
training_data.append({"class":"generic", "sentence":"how is it going today?"})

training_data.append({"class":"generic", "sentence":"have a nice day"})
training_data.append({"class":"generic", "sentence":"see you later"})
training_data.append({"class":"generic", "sentence":"have a nice day"})
training_data.append({"class":"generic", "sentence":"talk to you soon"})

training_data.append({"class":"generic", "sentence":"make me a sandwich"})
training_data.append({"class":"generic", "sentence":"can you make a sandwich?"})
training_data.append({"class":"generic", "sentence":"having a sandwich today?"})
training_data.append({"class":"generic", "sentence":"what's for lunch?"})

import csv

f = open('datasets/harassment_data_train.csv')
csv_f = csv.reader(f)

for row in csv_f:
  ##print (row)
  if row[1] == "harassment":
      training_data.append({"class":"harassment", "sentence":row[0]})
      print (row[0])
  if row[1] == "generic":
      training_data.append({"class":"generic", "sentence":row[0]})
      print (row[0])

f = open('datasets/harassment_data_train2.csv')
csv_f = csv.reader(f)

for row in csv_f:
  ##print (row)
  if row[1] == "harassment":
      training_data.append({"class":"harassment", "sentence":row[0]})
      print (row[0])
  if row[1] == "generic":
      training_data.append({"class":"generic", "sentence":row[0]})
      print (row[0])

f = open('datasets/harassment_data_train3.csv')
csv_f = csv.reader(f)

for row in csv_f:
  ##print (row)
  if row[1] == "harassment":
      training_data.append({"class":"harassment", "sentence":row[0]})
      print (row[0])
  if row[1] == "generic":
      training_data.append({"class":"generic", "sentence":row[0]})
      print (row[0])

f = open('datasets/harassment_data_train4.csv')
csv_f = csv.reader(f)

for row in csv_f:
  ##print (row)
  if row[1] == "harassment":
      training_data.append({"class":"harassment", "sentence":row[0]})
      print (row[0])
  if row[1] == "generic":
      training_data.append({"class":"generic", "sentence":row[0]})
      print (row[0])



print ("%s sentences in training data" % len(training_data))

words = []
classes = []
documents = []
ignore_words = ['?']
# loop through each sentence in our training data
for pattern in training_data:
    # tokenize each word in the sentence
    w = nltk.word_tokenize(pattern['sentence'])
    # add to our words list
    words.extend(w)
    # add to documents in our corpus
    documents.append((w, pattern['class']))
    # add to our classes list
    if pattern['class'] not in classes:
        classes.append(pattern['class'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = list(set(words))

# remove duplicates
classes = list(set(classes))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique stemmed words", words)


# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    output.append(output_row)

print ("# words", len(words))
print ("# classes", len(classes))


# sample training/output
i = 0
w = documents[i][0]
print ([stemmer.stem(word.lower()) for word in w])
print (training[i])
print (output[i])


import numpy as np
import time

# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)
 
def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

def think(sentence, show_details=False):
    x = bow(sentence.lower(), words, show_details)
    if show_details:
        print ("sentence:", sentence, "\n bow:", x)
    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(np.dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2

# ANN and Gradient Descent code from https://iamtrask.github.io//2015/07/27/python-network-part2/
def train(X, y, hidden_neurons=10, alpha=1, epochs=50000, dropout=False, dropout_percent=0.5):

    print ("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_percent if dropout else '') )
    print ("Input matrix: %sx%s    Output matrix: %sx%s" % (len(X),len(X[0]),1, len(classes)) )
    np.random.seed(1)

    last_mean_error = 1
    # randomly initialize our weights with mean 0
    synapse_0 = 2*np.random.random((len(X[0]), hidden_neurons)) - 1
    synapse_1 = 2*np.random.random((hidden_neurons, len(classes))) - 1

    prev_synapse_0_weight_update = np.zeros_like(synapse_0)
    prev_synapse_1_weight_update = np.zeros_like(synapse_1)

    synapse_0_direction_count = np.zeros_like(synapse_0)
    synapse_1_direction_count = np.zeros_like(synapse_1)
        
    for j in iter(range(epochs+1)):

        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))
                
        if(dropout):
            layer_1 *= np.random.binomial([np.ones((len(X),hidden_neurons))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))

        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = y - layer_2

        if (j% 10000) == 0 and j > 5000:
            # if this 10k iteration's error is greater than the last iteration, break out
            if np.mean(np.abs(layer_2_error)) < last_mean_error:
                print ("delta after "+str(j)+" iterations:" + str(np.mean(np.abs(layer_2_error))) )
                last_mean_error = np.mean(np.abs(layer_2_error))
            else:
                print ("break:", np.mean(np.abs(layer_2_error)), ">", last_mean_error )
                break
                
        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
        
        synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
        synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))
        
        if(j > 0):
            synapse_0_direction_count += np.abs(((synapse_0_weight_update > 0)+0) - ((prev_synapse_0_weight_update > 0) + 0))
            synapse_1_direction_count += np.abs(((synapse_1_weight_update > 0)+0) - ((prev_synapse_1_weight_update > 0) + 0))        
        
        synapse_1 += alpha * synapse_1_weight_update
        synapse_0 += alpha * synapse_0_weight_update
        
        prev_synapse_0_weight_update = synapse_0_weight_update
        prev_synapse_1_weight_update = synapse_1_weight_update

    now = datetime.datetime.now()

    # persist synapses
    synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(),
               'datetime': now.strftime("%Y-%m-%d %H:%M"),
               'words': words,
               'classes': classes
              }
    synapse_file = "synapses.json"

    with open(synapse_file, 'w') as outfile:
        json.dump(synapse, outfile, indent=4, sort_keys=True)
    print ("saved synapses to:", synapse_file)


X = np.array(training)
y = np.array(output)

start_time = time.time()

train(X, y, hidden_neurons=40, alpha=0.1, epochs=200000, dropout=False, dropout_percent=0.2)

elapsed_time = time.time() - start_time
print ("processing time:", elapsed_time, "seconds")


# probability threshold
ERROR_THRESHOLD = 0.2
# load our calculated synapse values
synapse_file = 'synapses.json' 
with open(synapse_file) as data_file: 
    synapse = json.load(data_file) 
    synapse_0 = np.asarray(synapse['synapse0']) 
    synapse_1 = np.asarray(synapse['synapse1'])

def classify(sentence, show_details=False):
    results = think(sentence, show_details)

    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD ] 
    results.sort(key=lambda x: x[1], reverse=True) 
    return_results =[[classes[r[0]],r[1]] for r in results]
    print ("%s \n classification: %s" % (sentence, return_results))
    return return_results

classify("sudo make me a sandwich")
classify("how are you today?")
classify("talk to you tomorrow")
classify("who are you?")
classify("make me some lunch")
print ()
classify("how was your lunch?", show_details=True)
classify("you play with your pussy and watch", show_details=True)

while True:
    line = input('Enter your input sentence for classification:')
    if line=="exit":
        break
    classify(line, show_details=True)


while True:
    filename = input('Enter candidate file path for classification:')
    if line=="exit":
        break
    ##filename = sys.argv[1]

    with open(filename, 'r') as f:
        datastore = json.load(f)

    for line in datastore["data"]:
        print (line)
        rr =classify(line)
        print (rr[0][0])


app = Flask(__name__)
CORS(app)

@app.route("/classify", methods=['POST'])
def classify_serve():
    """Respond to incoming calls with a brief message."""

    ##resp = "Ok"

    req_data = request.get_json()

    text = req_data["text"]
    author = req_data["author"]

    print (" i received " + text)
    print (" from " + author)

    combotext = author + "|" + text
    signature = hashlib.md5(combotext.encode('utf-8')).hexdigest()

    print (signature)


    rr =classify(text)

    url = "http://10.24.148.214:3000"

    payload = '{"name": "' + signature +'"}'
    headers = {
        'Content-Type': "application/json"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    injson = json.loads(response.text)

    out_r = {}
    out_r["status"] = "ok"
    out_r["class"] = rr[0][0]
    out_r["confidence"] = rr[0][1]
    out_r["transid"] = injson["data"]["id"]
    out_r["blockid"] = injson["data"]["blockId"]

    response = make_response(json.dumps(out_r))
    response.headers['content-type'] = 'application/json'

    return response

@app.route("/classifyGCP", methods=['POST'])
def classify_serve2():
    """Respond to incoming calls with a brief message."""

    ##resp = "Ok"

    os.system ('$env:GOOGLE_APPLICATION_CREDENTIALS="F:\data\hackprinceton\gc.json"')
    
    req_data = request.get_json()

    text = req_data["text"]
    author = req_data["author"]

    print (" i received " + text)
    print (" from " + author)

    combotext = author + "|" + text
    signature = hashlib.md5(combotext.encode('utf-8')).hexdigest()

    print (signature)

    commandline = 'python predictMLv3.py "' + text +'" aiot-fit-xlab TCN3380722269616129492 '

    print (commandline)

    os.system(commandline)

    with open("class.txt") as fp:  
       line = fp.readline()
    cls = line.strip()

    with open("confidence.txt") as fp:  
       line = fp.readline()
    con = line.strip()

    url = "http://10.24.148.214:3000"

    payload = '{"name": "' + signature +'"}'
    headers = {
        'Content-Type': "application/json"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    injson = json.loads(response.text)


    
    out_r = {}
    out_r["status"] = "ok"
    out_r["class"] = cls
    out_r["confidence"] = con
    out_r["transid"] = injson["data"]["id"]
    out_r["blockid"] = injson["data"]["blockId"]
    

    response = make_response(json.dumps(out_r))
    response.headers['content-type'] = 'application/json'

    return response





if __name__ == "__main__":
    app.run(debug=True, port = 8001)
    ##app.run(debug=True, host = '169.62.204.155', port = 8001)



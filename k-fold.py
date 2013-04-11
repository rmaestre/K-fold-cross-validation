# -*- coding: utf-8 -*-
import json
import pickle
import random
import math

# Import vectors previusly getted from MongoDB
vectors = pickle.load(open("data/vectors.p", "rb"))

# Shuffle the dict keys
rand_keys = []
keys = list(vectors.keys())
i = 0
while len(keys) > 0:
    element = random.choice(keys)
    keys.remove(element)
    rand_keys.append(element)
    i += 1

# Parameters
k = 40
min_limit = 0
max_limit = min_limit + k
errors = []

# Exceute k-fold test
while max_limit <= len(vectors):
    
    # DS to manage information
    vectors_to_testing = {}
    entity_frecuency = {}
    cont_training = 0
    cont_sample = 0
    cont_total = 0
    
    # Run k-fold testing
    for id in rand_keys:
        # Sampling
        if cont_total >= min_limit and cont_total < max_limit:
            cont_sample += 1
            vectors_to_testing[cont_sample] = {}
            vectors_to_testing[cont_sample]["supervised"] = vectors[id]["supervised_tags"]
            vectors_to_testing[cont_sample]["text"] = vectors[id]["text"]
        else:
            # Update model with training vectors
            for entity in vectors[id]["supervised_tags"]:
                if entity not in entity_frecuency:
                    entity_frecuency[entity] = 1
                else:
                    entity_frecuency[entity] += 1
            cont_training += 1
        cont_total += 1
    #print("Training vectors: %s" % cont_training)   
    #print("Sampling vectors: %s" % cont_sample) 

    error = []
    for id in vectors_to_testing:
        entities = vectors_to_testing[id]["supervised"]
        raw_text = vectors_to_testing[id]["text"][0]+" "+vectors_to_testing[id]["text"][1]
        n = len(entities)
        flatten_entity = []
        for entity in entities:
            if raw_text.find(entity) != -1:
                flatten_entity.append(entity)
        #print("Testing vector with %s/%s into the text" % (len(flatten_entity), n))
        #print("%s" % (float(len(flatten_entity))/float(n)))
    
        # Starting test
        if len(flatten_entity) > 0:
            succes = 0
            for entity in flatten_entity:
                if entity in entity_frecuency:
                    succes += 1
                else:
                    pass
            error.append(float(succes)/len(flatten_entity))
        
    print(sum(error)/float(cont_sample))
    errors.append(sum(error)/float(len(error)))
    
    # Update k-fold iteration
    min_limit += k
    max_limit += k
    
# Calculate mean and sd from errors
n = float(len(errors))
mean = sum(errors) / n
deviation = 0
for error in errors:
    deviation += pow((float(error - mean)), 2)
std_deviation = math.sqrt(deviation) * 1/n
print("Mean: %f\tDS:%f" % (mean, std_deviation))


    
    
    
    
'''
Created on Apr 25, 2013

@author: avneeshsarwate
'''
import Levenshtein as lv
import phrase
import random
import features

p = lv.randgen()
varList = []
varList.append(p)
featlist = []
for i in range(100):
    v = lv.supermorph(varList[random.randrange(len(varList))], 10)
    varList.append(v)
    features.phraseToScore(v)
    #featlist.append(features.vect(features.phraseToScore(v)))
print "done"

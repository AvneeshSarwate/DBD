'''
Created on Apr 15, 2013

@author: avneeshsarwate
'''
import phrase

p = phrase.Phrase()

p.append((60, 1))
p.append((65, 1))
p.append((67, 1))
p.append((63, 1))
p.append((62, 1))

phrase.play(p)
#!/usr/bin/env python
def volume(pos):
    '''Returns volume of a given object co-ordinates'''
    l = abs(pos['l1'] - pos['l2'])
    b = abs(pos['b1'] - pos['b2'])
    h = abs(pos['h1'] - pos['h2'])    
    return l*b*h
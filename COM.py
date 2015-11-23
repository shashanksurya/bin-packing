#!/usr/bin/env python
'''This program is used for calculating center of mass'''
import random

def COM(obj_list):
	'''Calculate center of mass for given set of objects'''
	com_obj = {}
	sum_of_masses = 0
	xc = 0
	yc = 0
	zc = 0
	for eachobj in obj_list:
		xc += eachobj['x']*eachobj['mass']
		yc += eachobj['y']*eachobj['mass']
		zc += eachobj['z']*eachobj['mass']
		sum_of_masses += eachobj['mass']
	com_obj['x'] = xc / sum_of_masses
	com_obj['y'] = yc / sum_of_masses
	com_obj['z'] = zc / sum_of_masses
	return com_obj

if __name__ == '__main__':
	obj_list = []
	for i in range(0,3):
		temp = {}
		temp['x'] = random.uniform(1.0,20.0)
		temp['y'] = random.uniform(1.0,20.0)
		temp['z'] = random.uniform(1.0,20.0)
		temp['mass'] = random.randrange(1,50)
		obj_list.append(temp)
	print(obj_list)
	print(COM(obj_list))

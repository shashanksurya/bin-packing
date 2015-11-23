#!/usr/bin/env python
''' This program divides a list with weights
into two approximately equal subsets

1. Sort the list
2. Create two lists and maintain their sums
3. Add largest element from parent list to smaller child list
4. Update sum and repeat
5. Stop when one reaches n/2 and add remaining to other child list
'''
import random

def create_random_list(x):
	'''Create a random list of x objects with each object in the range of 1-10'''
	temp = []
	for i in range(0,x):
		if i%2 == 0:
			temp.append(random.randrange(1,5))
		else:
			temp.append(random.randrange(5,10))
	return temp

def divider(l):
	'''Divide the given list into two lists which has approximately equal sum'''
	return_dict = {}
	temp1 = []
	temp2 = []
	index = 1
	l.sort(reverse = True)
	temp1.append(l[0])
	#print("Parent List sum: "+str(sum(l))+" Length: "+str(len(l)))
	while(1):
		if (len(temp1) < len(l)/2) and (len(temp2) < len(l)/2):
			if sum(temp1) > sum(temp2):
				temp2.append(l[index])
				index+=1
			else:
				temp1.append(l[index])
				index+=1
		else:
			while index!=len(l):
				if len(temp1) < len(l)/2:
					temp1.append(l[index])
					index+=1
				else:
					temp2.append(l[index])
					index+=1
			break
	#print("List 1 sum: "+str(sum(temp1))+" Length: "+str(len(temp1)))
	#print("List 2 sum: "+str(sum(temp2))+" Length: "+str(len(temp2)))
	return_dict['list1'] = temp1
	return_dict['list2'] = temp2
	return return_dict
	
if __name__ == '__main__':
	l = create_random_list()
	divider(l)
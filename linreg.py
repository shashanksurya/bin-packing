import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def draw_regression(xx,yy):
	'''Create a scatter plot based on data'''
	n = 50
	x = np.array(xx)
	y = np.array(yy)
	fig, ax = plt.subplots()
	fit = np.polyfit(x, y, deg=1)
	ax.plot(x, fit[0] * x + fit[1], color='red')
	ax.scatter(x, y)
	fig.show()

def print_curve_props(x,y):
	'''Prints the regression model properties'''
	slope, intercept, rvalue, pvalue,stderr = linregress(x,y)
	print "r squared: "+str(rvalue**2)
	print "pvalue: " + str(pvalue)
	print "slope: " + str(slope)
	print "intercept: " + str(intercept)
	print "stderr: " + str(stderr)
	print "Total points considered: " + str(len(x))

def main(filename):
	'''Opens the parsed data and fits it to linear regression model'''
	x = []
	y = []
	f = open(filename,"r")
	data = f.readlines()
	for line in data:
		temp = line.split()
		y.append(float(temp[0]))
		x.append(float(temp[1]))
	draw_regression(x,y)
	print_curve_props(x,y)

if __name__ == '__main__':
	main()

'''
200 dataset
LinregressResult(slope=-447.32359011352338, intercept=14503.019022184453, rvalue=-0.98475169085347714, pvalue=1.3556765627845491e-151, stderr=5.6302267778460307)'''
'''
Auxiliary functions used in Assignment 2 - Machine Learning Pipeline 
CAPP 30254 1 Machine Learning for Public Policy

Author: Jesus I. Ramirez Franco
''' 

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score as accuracy


def histogram(df, variable, num_of_bins):
	'''
	Creates the histogram of a variable
	Inputs:
		- df (Pandas data frame): data frame that contains the variable 
		  we want to explore.
		- variable (string): name of the variable of which we want to
		  create the histogram.
		- num_of_bins (integer): number of intervals to be used in the 
		  histogram.
	Returns a plot.
	'''
	plt.hist(df[variable], bins = num_of_bins)
	plt.title('Distribution of ' + variable)
	plt.xlabel(variable)
	plt.ylabel('Frequency')
	return plt.show()


def boxplot (df, variable):
	'''
	Creates a box plot of a variable of interest
	Inputs:
		- df (Pandas data frame): data frame that contains the variable 
		  we want to explore.
		- variable (string): name of the variable of which we want to
		  create the box plot.
	Returns a plot
	'''
	plt.boxplot(df[variable])
	plt.title(variable + ' box plot')
	return plt.show()


def exploratory_plots(df, variable, num_of_bins):
	'''
	Creates the histogram and the box plot of a variable of interest.
	Inputs:
		- df (Pandas data frame): data frame that contains the variable 
		  we want to explore.
		- variable (string): name of the variable of which we want to
		  create the histograma and the box plot.
		- num_of_bins (integer): number of intervals to be used in the 
		  histogram.
	Returns a plot
	'''
	return histogram(df, variable, num_of_bins), boxplot (df, variable)


def scatter(df, dependent_variable, feature):
	'''
	Creates a scatter plot for a dependent variable and a independent 
	variable.
	Inputs:
		- df (Pandas data frame): data frame that contains the variables 
		  we want to explore.
		- dependent_variable (string): name of the dependent variable.
		- feature (string): name of the independent variable.
	Returns a plot 
	'''
	plt.scatter(df[dependent_variable], df[feature])
	plt.title(feature + ' vs ' + dependent_variable)
	plt.ylabel(feature)
	plt.xlabel(dependent_variable)
	return plt.show()


def discretize(df, variable):
	'''
	Discretize a continuous variable.
	Inputs:
		- df (Pandas data frame): data frame that contains the variable that we
		  want to convert.
		- variable (string): name of the variable we want to convert.
	Returns a modified data frame.
	'''
	df[variable] = df[variable].apply(lambda x: int(round(x,0)))


def binaryze(df, variable, threshold):
	'''
	takes a categorical variable and create binary/dummy variables from it.
	Inputs:
		- df (Pandas data frame): data frame that contains the variable that we
		  want to convert.
		- variable (string): name of the variable we want to convert.
	Returns a modified data frame.
	'''
	df[variable] = df[variable].apply(lambda x: True if x > threshold else False)

def get_myaccuracy(predicted_array, observed_array):
	'''
	Computes the accuracy of a model.
	Inputs:
		- predicted_array (list): array with the predicted values.  
		- observed_array (pandas.series): array with the actual values
	Returns a float.
	'''
    correct_predictions = 0
    for i in range(len(predicted_array)):
        if predicted_array[i] == observed_array.iloc[i]:
            correct_predictions +=1
    accuracy = correct_predictions/len(predicted_array)
    return round(accuracy, 2)

def get_accuracy_table(criterion_list, splitter_list, max_depth_list, x_train, x_test, y_train, y_test):
	'''
	Creates a data frame with the information of the parameter of the models 
	and its accuracy.
	Inputs:
		- criterion_list (list of strings): list of different criterion to be 
		  used in the models.
		- splitter_list (list of strings): list of different splitters to be 
		  used in the models
		- max_depth_list (list): list of the different values to be used in 
		  the model
		- x_train (data frame): independent variables training set.
		- x_test (data frame): independent variables testing set.
		- y_train (data frame): dependent variable training set.
		- y_test (data frame): dependent variable testing set.
	Returns a data frame
	'''
	results_list = []
	for criterion in criterion_list:
		for splitter in splitter_list:
			for depth in max_depth_list:
				dec_tree = DecisionTreeClassifier(criterion=criterion, splitter=splitter, max_depth=depth)
				dec_tree.fit(x_train, y_train)
				results_list.append([criterion, splitter, depth, accuracy(dec_tree.predict(x_train), y_train), 
					accuracy(dec_tree.predict(x_test), y_test)])
	df = pd.DataFrame(results_list)
	df.columns = ['criterion', 'splitter', 'max_depth', 'accuracy_train', 'accuracy_test']
	return df
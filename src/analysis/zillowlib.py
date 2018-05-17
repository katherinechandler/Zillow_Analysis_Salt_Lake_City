# library of functions used in zillow statistical analysis

from statsmodels.stats.multicomp import pairwise_tukeyhsd
import csv
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sm
import statsmodels.graphics as smg
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import scipy.stats
import datetime
import itertools


# define a function to sumarize confidence intervals for mean metric value for data given a certain cut

def summarize_tukey(data, cuts, metrics):
    for cut in cuts:
        for metric in metrics:
            print('Tukey\'s HSD test for {} and {}'.format(cut, metric))
            t = pairwise_tukeyhsd(endog=data[metric], groups=data[cut], alpha=0.05)
            print(t.summary())

# define a function that will identify only statistically significant differences between categories
# based on Tukey's HSD of a for a given data set, data cut, and numeric metric
def summarize_tukey_significant(data, cuts, metrics):
    for cut in cuts:
        for metric in metrics:
            print('\nTukey\'s HSD test for {} and {}'.format(cut, metric))
            t = pairwise_tukeyhsd(endog=data[metric], groups=data[cut], alpha=0.05)
            data_as_csv = t._results_table.as_csv()
            for row in csv.reader(data_as_csv.split("\n")):
                if len(row) > 4 and row[5] == 'True  ':
                    print(row[0]+" "+row[1]+" "+row[5])

# define a function to plot confidence intervals for mean metric value for data given a certain cut
def plot_tukey(data, cuts, metrics):
    for cut in cuts:
        for metric in metrics:
            pairwise_tukeyhsd(endog=data[metric], groups=data[cut], alpha=0.05).plot_simultaneous(figsize=(4, 4))
            plt.title('Tukey\'s HSD test for {} and {}'.format(cut, metric))


# create a function to perform pairwise two tailed t-test on
# a given data set, data cut, and metric
def calc_pval(data, cut, metric):
    groups = list(itertools.combinations(data[cut].unique(), 2))
    for n in groups:
        data1 = data[data[cut]==n[0]][metric]
        data2 = data[data[cut]==n[1]][metric]
        t1 = scipy.stats.ttest_ind(a= data1, b= data2, equal_var=False)
        print('p-val =', t1[1], 'for {}, {}'.format(n[0], n[1]))


#individually calculate the p-value in price difference between 84103 and all other listings

def specific_p_calc(location, cut, metric, data):
    data_specific = data[data[cut] == location]
    data_remainder = data[data[cut] != location]
    t1 = stats.ttest_ind(a= data_specific[metric],
                            b= data_remainder[metric],
                            equal_var=False)
    print('the p-value for {} compared to all other {} is'.format(location, cut), t1[1])


# create a function to perform pairwise two tailed t-test on
# a given data set, data cut, and metric on each bedroom type

def calc_pval_comps(data, cut, metric):
    groups = list(itertools.combinations(data[cut].unique(), 2))
    for n in groups:
        for bed in range(1,6):
            data1 = data[(data[cut]==n[0]) & (data['beds']==bed)][metric]
            data2 = data[(data[cut]==n[1]) & (data['beds']==bed)][metric]
            t1 = scipy.stats.ttest_ind(a= data1, b= data2, equal_var=False)
            if t1[1]<=0.05:
                print('p-val =', t1[1], 'for {} bedrooms in {}, {}'.format(bed, n[0], n[1]))
            else:
            	print('{} bedrooms in {}, {} are not significantly different'.format(bed, n[0], n[1]))          
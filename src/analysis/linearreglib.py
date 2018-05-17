# library of functions used in zillow linear regression analysis
import pandas as pd
import itertools
import statsmodels.api as sm


# function to create dummies in df for specific variable

def create_dummies(data, dummy_var):
    data_dummies = pd.get_dummies(data, columns=[dummy_var])
    return(data_dummies)

# function to format formula for regression model based on data, variable to predict, and a list of variables to 
# use in building the model

def create_formula(data, dep_var, var_list):
    column_list = list(data.columns)
    model_list=[]
    #loop over column headings to create list of variables desired in model (and exclude dependant variable)
    for item in column_list:
        if item == dep_var:
            pass
        elif item in var_list:
            model_list.append(item)
    regression_formula = '{} ~ '.format(dep_var) + ' + '.join(model_list)
    return(regression_formula)

# fit an OLS model from a formula

def create_OLS_model(formula, data):
    results = sm.OLS.from_formula(formula, data).fit()
    return(results)

# this function integrates dummy variable generation and model fitting given a set of 
# data, the desired dummy variable, the dependant variable, and a list of variables omitted from the analyses

def sumarize_single_OLS_model_stats(data, dummy_var, dep_var, var_list):
    data_dummies = create_dummies(data, dummy_var)
    formula = create_formula(data_dummies, dep_var, var_list)
    results = create_OLS_model(formula, data_dummies)
    model_info = {}
    model_info['formula']=formula
    model_info['r_squared']=results.rsquared
    model_info['num_sig_variables']=len(results.pvalues[results.pvalues<0.05])
    model_info['total_num_variables']=len(results.pvalues)
    model_info['ratio_vars_significant']= (len(results.pvalues[results.pvalues<0.05]))/len(results.pvalues)
    return(model_info)

# function to make all combos of 2 or more variables from a list of features, and adds dummy variables to 
# each set of combinations; use this function if generating dummies

def generate_feature_combinations_dummy_added(data, dummy_var, dep_var_list):
    feature_combinations = []
    feature_combinations_list=[]
    orig_list = data.columns
    dummy_list = (create_dummies(data, dummy_var)).columns
    dummy_vars_only = []
    for item in dummy_list:
        if item not in orig_list:
            dummy_vars_only.append(item)
    columns_dep_var_removed = data.columns.drop(dep_var_list).drop(dummy_var)
    for n in range(2,len(columns_dep_var_removed)):
        combos = list(itertools.combinations(columns_dep_var_removed, n))
        feature_combinations.append(combos)
        for first_list in feature_combinations:
            for feature_tup in first_list:
                output = list(feature_tup) + dummy_vars_only
                feature_combinations_list.append(output)
    return(feature_combinations_list)


# function to make all combos of 4 or more variables from a list of features, does not add dummy variables
# unless explicitly given dummies as data; use generate_feature_combinations_dummy_added if dummies were made

def generate_feature_combinations(data, dep_var_list):
    feature_combinations = []
    feature_combinations_list=[]
    columns_dep_var_removed = data.columns.drop(dep_var_list)
    
    for n in range(2,len(columns_dep_var_removed)):
        combos = list(itertools.combinations(columns_dep_var_removed, n))
        feature_combinations.append(combos)
        for first_list in feature_combinations:
            for feature_tup in first_list:
                output = list(feature_tup)
                feature_combinations_list.append(output)
    return(feature_combinations_list)

# this function runs summarize_OLS_model_stats for a single dummy variable, list of dependant variables, 
# and list of feature combinations and returns results in df for sorting

def sumarize_multi_OLS_models(data, dummy_var, dep_var_list, feature_combinations):
    n=1
    model_dict = {}
    for dep in dep_var_list:
        for feature_group in feature_combinations:
            model_name = 'model_{}, dep={}, dummy={}'.format(n,dep,dummy_var)
            model_dict[model_name] = sumarize_single_OLS_model_stats(data, dummy_var, dep, feature_group)
            n+=1
    return(pd.DataFrame.from_dict(model_dict, orient='index'))
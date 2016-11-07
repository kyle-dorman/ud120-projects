import numpy as np
import sys

def findPersonsSimilarToLastName(myDict, lastName):
    result = []
    for key, value in myDict.iteritems():
        if lastName.lower() in key.lower():
            result.append(value)
    return result
    
    
def orig_pois():
    poi = []
    with open("../final_project/poi_names.txt", "r") as f:
        for item in f:
            if item[0] != '(': continue
            items = item.strip().split(' ')
            items.pop(0)
            items = ''.join(items).split(',')
            items = ' '.join(items)
            items = items.upper()

            poi.append(items)

    return poi

def reduceToFeature(data, feature, include_poi=True, include_non_poi=True):
    return np.array([value[feature] for value in data.itervalues() if value[feature] != 'NaN'
                     and ((include_poi and value['poi']) 
                          or (include_non_poi and not value['poi']))])

def nanCount(data, feature, include_poi=True, include_non_poi=True):
    return len([0 for value in data.itervalues() if value[feature] == 'NaN'
                     and ((include_poi and value['poi']) 
                          or (include_non_poi and not value['poi']))])
    
def nonNanCount(data, feature, include_poi=True, include_non_poi=True):
    return len(reduceToFeature(data, feature, include_poi, include_non_poi))
    
def mean(data, feature, include_poi=True, include_non_poi=True):
    d = reduceToFeature(data, feature, include_poi, include_non_poi)
    for item in d:
        if isinstance(item, basestring):
            return 'NaN'
        
    if len(d) > 0:
        return np.mean(d)
    else:
        return 'NaN'

def std(data, feature, include_poi=True, include_non_poi=True):
    d = reduceToFeature(data, feature, include_poi, include_non_poi)
    for item in d:
        if isinstance(item, basestring):
            return 'NaN'
    if len(d) > 0:
        return np.std(d)
    else:
        return 'NaN'

def max(data, feature, include_poi=True, include_non_poi=True):
    d = reduceToFeature(data, feature, include_poi, include_non_poi)
    for item in d:
        if isinstance(item, basestring):
            return 'NaN'
    if len(d) > 0:
        return np.max(d)
    else:
        return 'NaN'

def min(data, feature, include_poi=True, include_non_poi=True):
    d = reduceToFeature(data, feature, include_poi, include_non_poi)
    for item in d:
        if isinstance(item, basestring):
            return 'NaN'
    if len(d) > 0:
        return np.min(d)
    else:
        return 'NaN'

def basicFeatureInfo(data, feature, include_poi=True, include_non_poi=True):
    return {
        'nanCount'    : nanCount(data, feature, include_poi, include_non_poi),
        'nonNanCount' : nonNanCount(data, feature, include_poi, include_non_poi),        
        'mean'        : mean(data, feature, include_poi, include_non_poi),  
        'std'         : std(data, feature, include_poi, include_non_poi),  
        'max'         : max(data, feature, include_poi, include_non_poi),        
        'min'         : min(data, feature, include_poi, include_non_poi)
    }

def basicFeatureInfoByType(data, feature):
    return {
        'poi': basicFeatureInfo(data, feature, True, False),
        'non_poi': basicFeatureInfo(data, feature, False, True),
        'all': basicFeatureInfo(data, feature)
    }

def allDataInfo(data):
    results = {}
    firstPoint = data[data.keys()[0]]
    for key in firstPoint.iterkeys():
        results[key] = basicFeatureInfoByType(data, key)
    return results

def maxPersonForFeature(data, feature):
    max_perp = 'NaN'
    max_val = float(-sys.maxint)
    for key, value in data.iteritems():
        if value[feature] == 'NaN':
            continue
        if max_val < float(value[feature]):
            max_val = float(value[feature])
            max_perp = key
    return max_perp

def maxPersonForFeature(data, feature):
    max_perp = 'NaN'
    max_val = float(-sys.maxint)
    for key, value in data.iteritems():
        if value[feature] == 'NaN':
            continue
        if isinstance(value[feature], basestring):
            return 'NaN'
        if max_val < float(value[feature]):
            max_val = float(value[feature])
            max_perp = key
    return max_perp

def minPersonForFeature(data, feature):
    min_perp = 'NaN'
    min_val = float(sys.maxint)
    for key, value in data.iteritems():
        if value[feature] == 'NaN':
            continue
        if isinstance(value[feature], basestring):
            return 'NaN'
        if min_val > float(value[feature]):
            min_val = float(value[feature])
            min_perp = key
    return min_perp

def personMaxMinCount(data):
    results = {
        'max' : {},
        'min' : {} 
    }
    firstPoint = data[data.keys()[0]]
    for key in firstPoint.iterkeys():
        minPerson = minPersonForFeature(data, key)
        maxPerson = maxPersonForFeature(data, key)
        if minPerson in results['min']:
            results['min'][minPerson] = results['min'][minPerson] + 1
        else:
            results['min'][minPerson] = 1
        
        if maxPerson in results['max']:
            results['max'][maxPerson] = results['max'][maxPerson] + 1
        else:
            results['max'][maxPerson] = 1

    return results

financial_features = ['salary',
 'deferral_payments',
 'total_payments',
 'exercised_stock_options',
 'bonus',
 'restricted_stock',
 'restricted_stock_deferred',
 'total_stock_value',
 'expenses',
 'loan_advances',
 'other',
 'director_fees',
 'deferred_income',
 'long_term_incentive']

numerical_email_features = [
 'to_messages',
 'shared_receipt_with_poi',
 'from_messages',
 'from_this_person_to_poi',
 'from_poi_to_this_person']



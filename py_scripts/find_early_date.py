"""Python Libraries"""
from glob import glob
from re   import findall

def find_early_date():
    '''Search for the minimum date of the source files'''
    X = glob('*.txt')
    if len(X) > 1:
        X = min(findall("\d+", '{}'.format(X)))
    else:
        X = ''.join(findall("\d+", '{}'.format(X)))
    DT = X[4:8] + '-' + X[2:4] + '-' + X[0:2]
    return X,DT
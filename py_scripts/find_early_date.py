import glob
import re

#Поиск минимальной даты файлов-источников
def find_early_date():
    X = glob.glob('*.txt')
    if len(X) > 1:
        X = min(re.findall("\d+", '{}'.format(X)))
    else:
        X = ''.join(re.findall("\d+", '{}'.format(X)))
    DT = X[4:8] + '-' + X[2:4] + '-' + X[0:2]
    return X,DT
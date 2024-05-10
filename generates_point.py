import numpy as np
import itertools
import os

paradict = {
        #'projectile' : 'randnucl',
        #'projectile' : 'randnucl',
        #'number-events' : '1000000',
        'reduced-thickness' : '0.007',
        'fluctuation' : '1.6',
        'nucleon-width' : '0.5',
        'cross-section' : '4.23',
        'normalization' : '5.6',
        'meanbeta3' : '0',
        'sigmabeta3' : '0',
        'sigmabeta4' : '0',
        'meangamma' : '0',
        'sigmagamma' : '0',
            }

change_para_dict = {
        'meanR' : [6.0, 7.0, 3],
        'meana' : [0.4, 0.7, 2],
        'meanbeta2' : [0.18, 0.28, 3],
        'meanbeta4' : [0.0, 0.12, 2],
        'sigmaR' : [0.0, 1.0, 3],
        'sigmaa' : [0.0, 0.1, 2],
        'sigmabeta2' : [0.0, 0.08, 2],
}

def write_file(paraname_list,product,event_number):
    tem_dict = paradict
    for i in range(0,len(paraname_list)):
        tem_dict.update({paraname_list[i]:product[i]})
    with open('./data/parameter_{}'.format(event_number),'w') as f:
        for key in tem_dict:
            f.write('{}  {} \n'.format(key, tem_dict[key]))
    


def generate_para(paradict,change_para_dict):
    paraname_list = []
    parares_list = []
    for key in change_para_dict:
        paraname_list.append(key)
        parares_list.append(np.linspace(change_para_dict[key][0],
                                            change_para_dict[key][1],
                                            change_para_dict[key][2]))
    event_number = 0
    for product in itertools.product(*parares_list):
        event_number += 1
        write_file(paraname_list,product,event_number)

generate_para(paradict,change_para_dict)

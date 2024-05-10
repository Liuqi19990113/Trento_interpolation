import numpy as np
from multiprocessing.pool import Pool
import sys
import os
import time


def event_file_reader(text_path):
    this_data = np.loadtxt(text_path)
    mult = this_data[:,3]
    e2 = this_data[:,4]
    e3 = this_data[:,5]
    e4 = this_data[:,6]
    d_npart = this_data[:,8]
    return np.column_stack((mult,e2,e3,e4,d_npart))


def sorter(results_array):
    final_list = []
    sorted_result = results_array[np.argsort(results_array[:,0])][::-1]
    #print(sorted_result)
    centrality = np.array([0,5,10,20,30,40,50,60])
    cut_order = len(sorted_result)*0.01*centrality
    for i in range(0,len(cut_order)-1):
        print('In centrality {}'.format(i))
        first_cut = int(cut_order[i])
        last_cut = int(cut_order[i+1])
        this_cut_tmp_array = sorted_result[first_cut:last_cut]
        tem_e2_array = this_cut_tmp_array[:,1]
        tem_e3_array = this_cut_tmp_array[:,2]
        tem_e4_array = this_cut_tmp_array[:,3]
        tem_pT_array = this_cut_tmp_array[:,4]
        e2_sq = tem_e2_array*tem_e2_array
        e3_sq = tem_e3_array*tem_e3_array
        e4_sq = tem_e4_array*tem_e4_array
        e2_4 = np.power(tem_e2_array,4)
        e3_4 = np.power(tem_e3_array,4)
        e2_6 = np.power(tem_e2_array,6)
        c22 = (np.mean(e2_sq))
        c32 = (np.mean(e3_sq))
        c42 = (np.mean(e4_sq))
        c24 = np.mean(e2_4) - 2*np.mean(e2_sq)*np.mean(e2_sq)
        c34 = np.mean(e3_4) - 2*np.mean(e3_sq)*np.mean(e3_sq)
        c26 = np.mean(e2_6) - 9*np.mean(e2_4)*np.mean(e2_sq) + 12*np.power(np.mean(e2_sq),3)
        mean_pT = np.mean(tem_pT_array)
        delta_pT_sq = np.mean(np.power((tem_pT_array-mean_pT),2))
        delta_pT_3 = np.mean(np.power((tem_pT_array-mean_pT),3))
        cov_v2sq_pT = np.mean(e2_sq*(tem_pT_array-mean_pT))
        cov_v2sq_pT2 = np.mean(e2_sq*np.power((tem_pT_array-mean_pT),2))
        cov_v2p4_pT = np.mean(e2_4*(tem_pT_array-mean_pT))
        final_list.append([c22,c32,c42,c24,c34,c26,mean_pT,delta_pT_sq,
                           delta_pT_3,cov_v2sq_pT,cov_v2sq_pT2,cov_v2p4_pT])
    print('end function sorter')
    return np.array(final_list)



if __name__ =='__main__':
    t1 = time.time()
    events_path = os.path.abspath(sys.argv[1])
    print('Begin!')
    all_data_array = event_file_reader(events_path)
    splited_array = np.array_split(all_data_array,4,axis=0)
    final_results = []
    for one_data_array in splited_array:
        print('Data shape = {}'.format(np.shape(one_data_array)))
        print('Begin sort function!')
        result = sorter(one_data_array)
        final_results.append(result)
    final_results = np.array(final_results)
    print('Final results shape = {}'.format(np.shape(final_results)))
    mean_value = np.zeros((np.shape(final_results)[1],np.shape(final_results)[2]))
    std_err = np.zeros((np.shape(final_results)[1],np.shape(final_results)[2]))
    for i in range(0,np.shape(final_results)[1]):
        for j in range(0,np.shape(final_results)[2]):
            mean_value[i,j] = np.mean(final_results[:,i,j])
            std_err[i,j] = np.std(final_results[:,i,j])
    t2 = time.time()
    print('mean value:')
    print(mean_value)
    print('std error:')
    print(std_err)
    mean_1d = np.concatenate(mean_value.T,axis=0)
    stderr_1d = np.concatenate(std_err.T,axis=0)
    np.savetxt("{}/output.txt".format(os.path.dirname(events_path)),np.column_stack((mean_1d,stderr_1d)),delimiter=" ")
    print('Done!, time = {}s'.format(t2-t1))




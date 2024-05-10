import numpy as np
import os 
from scipy.interpolate import interpn
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

change_para_dict = {
        'meanR' : [6.0, 7.0, 3],
        'meana' : [0.4, 0.7, 2],
        'meanbeta2' : [0.18, 0.28, 3],
        'meanbeta4' : [0.0, 0.12, 2],
        'sigmaR' : [0.0, 1.0, 3],
        'sigmaa' : [0.0, 0.1, 2],
        'sigmabeta2' : [0.0, 0.08, 2],
}

obs_order = {'c22':0,'c32':1,'c42':2,'c24':3,'c34':4,'c26':5,
             'mean_pT':6,'delta_pT_sq':7,'delta_pT_3':8,'cov_v2sq_pT':9,
             'cov_v2sq_pT2':10,'cov_v2p4_pT':11}

para_points = []
for key in change_para_dict:
    para_points.append(np.linspace(change_para_dict[key][0],
                                        change_para_dict[key][1],
                                        change_para_dict[key][2]))



def read_res(event_name):
    data = np.loadtxt(event_name+'/output.txt')
    return data[:,0], data[:,1]


def read_and_reshape_predict_data(number_events,inter_point):
    mean_list = []
    stderr_list = []
    for i in range(1,number_events+1):
        mean, stderr = read_res('./data/event_{}'.format(i))
        mean_list.append(mean)
        stderr_list.append(stderr)
    mean_array = np.array(mean_list)
    stderr_array = np.array(stderr_list)
    inter_res = np.array([])
    inter_stderr = np.array([])
    for j in range(0,mean_array.shape[1]):
        this_data = np.reshape(mean_array[:,j],(3,2,3,2,3,2,2))
        this_stderr = np.reshape(stderr_array[:,j],(3,2,3,2,3,2,2))
        inter_res = np.append(inter_res,interpn(points=para_points,values=this_data,xi=inter_point,fill_value=True,bounds_error=False))
        inter_stderr = np.append(inter_stderr,interpn(points=para_points,values=this_stderr,xi=inter_point,fill_value=True,bounds_error=False))
    inter_res = np.reshape(inter_res,(12,7))
    inter_stderr = np.reshape(inter_stderr,(12,7))
    return inter_res,inter_stderr


def draw_inter(obs_name='c22'):
    x = [2.5,7.5,15,25,35,45,55]
    y = read_and_reshape_predict_data(432,[6.0,0.4,0.18,0.0,0.0,0.0,0.0])[0][obs_order[obs_name],:]
    fig, ax = plt.subplots()  
    l,=plt.plot(x,y,"or-")            
    plt.subplots_adjust(bottom=0.5,left=0.3)
    axcolor = 'lightgoldenrodyellow'  # slider的颜色
    meanR = plt.axes([0.15, 0.38, 0.65, 0.04], facecolor=axcolor) 
    meana = plt.axes([0.15, 0.33, 0.65, 0.04], facecolor=axcolor) 
    meanbeta2 = plt.axes([0.15, 0.28, 0.65, 0.04], facecolor=axcolor) 
    meanbeta4 = plt.axes([0.15, 0.23, 0.65, 0.04], facecolor=axcolor) 
    sigmaR = plt.axes([0.15, 0.18, 0.65, 0.04], facecolor=axcolor) 
    sigmaa = plt.axes([0.15, 0.13, 0.65, 0.04], facecolor=axcolor) 
    sigmabeta2 = plt.axes([0.15, 0.08, 0.65, 0.04], facecolor=axcolor)
    s1 = Slider(meanR, 'meanR', valmin= 6.0 , valmax= 7.0, valinit=6.0)
    s2 = Slider(meana, 'meana', valmin= 0.4, valmax = 0.7, valinit=0.4)
    s3 = Slider(meanbeta2, 'meanbeta2', valmin=0.18, valmax=0.28, valinit=0.18)
    s4 = Slider(meanbeta4, 'meanbeta4', valmin=0.0 , valmax=0.12, valinit=0.0)
    s5 = Slider(sigmaR, 'deltR', valmin = 0.0 , valmax=1.0, valinit=0.0)
    s6 = Slider(sigmaa, 'delta', valmin=0.0, valmax=0.1, valinit=0.0)
    s7 = Slider(sigmabeta2, 'deltbeta2', valmin=0.0, valmax=0.08, valinit=0.0)
    def update(val):
        s1_ = s1.val
        s2_ = s2.val
        s3_ = s3.val
        s4_ = s4.val
        s5_ = s5.val
        s6_ = s6.val
        s7_ = s7.val
        y=read_and_reshape_predict_data(432,[s1_,s2_,s3_,s4_,s5_,s6_,s7_])[0][obs_order[obs_name],:]
        l.set_ydata(y)
    fig.canvas.draw_idle()
    s1.on_changed(update) 
    s2.on_changed(update)
    s3.on_changed(update)
    s4.on_changed(update)
    s5.on_changed(update)
    s6.on_changed(update)
    s7.on_changed(update)
    plt.show()    

draw_inter('cov_v2sq_pT')
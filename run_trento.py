#!/user/bin/python3
# -*- coding: utf-8 -*-
#This python script used to run bayes analysis
import os
from multiprocessing.pool import Pool
import time

trento_parameters_dict = {
    "projectile" : "randnucl",
    "projectile" : "randnucl",
    "number-events" : 1000000,
    "cross-section" : 4.23,
    "nucleon-min-dist" : 0.0,
    "normalization" : 5.6,
    "reduced-thickness" : 1,
    "nucleon-width" : 0.956, 
    "fluctuation" : 0.5,
    "constit-number" : 1,
    "nucleon-min-dist" : 0.0,
    "meanR" : 6.7,
    "meana" : 0.5,
    "meanbeta2" : 0.25,
    "meanbeta3" : 0.1,
    "meanbeta4" : 0.09,
    "meangamma" : 0,
    "sigmaR": 0,
    "sigmaa": 0,
    "sigmabeta2": 0,
    "sigmabeta3": 0,
    "sigmabeta4": 0,
    "sigmagamma": 0
}

trento_path = "/home/hic-song/workstation/LiuQi/trento_nucstrc/trento/build/src/trento"


def dict_update(file_name):
    tem_dict = trento_parameters_dict
    with open(file_name,'r') as f:
        update_dict = {}
        for line in f :
            name, value = line.split()
            value = float(value)
            if name == "beta2":
                update_dict.update({"beta-2p" :value, "beta-2t" :value})
            elif name == "gamma":
                update_dict.update({"gammap" :value, "gammat" :value})
            else:
                update_dict.update({name :value})
        tem_dict.update(update_dict)
    return tem_dict

def write_parameter_file(para_dict,file_name):
    with open(file_name,'w') as g:
        for thing in para_dict.items():
            this_key = thing[0]
            this_value = thing[1]
            if this_key == "projectile":
                g.write("{} = {}\n".format(this_key,this_value))
            g.write("{} = {}\n".format(this_key,this_value))
    

def run_trento(para):
    para_folder = para[0]
    para_name = para[1]
    dir = para_name.split("_")[1]
    para_folder = os.path.abspath(para_folder)
    event_folder = os.path.join(para_folder,"event_{}".format(dir))
    os.mkdir(event_folder)
    os.system("mv {}/parameter_{}  {}/parameters.txt".format(para_folder ,dir, event_folder))
    this_event_dict = dict_update("{}/parameters.txt".format(event_folder,dir))
    trento_config_path = "{}/trento_config_{}".format(event_folder,dir)
    write_parameter_file(this_event_dict,trento_config_path)
    os.system("{} -c {} > {}/event_{}.out ".format(trento_path,trento_config_path,event_folder,dir))


def run_event(para_folder):
    para_list = [(para_folder,para_name) for para_name in os.listdir(para_folder)]
    with Pool() as pool:
        pool.map(run_trento,para_list)


def cal_obs(result):
    result_folder = result[0]
    result_file = result[1]
    os.system("python3 ./cal_obs.py {} > {}/cal.log".format(result_file, result_folder))


def run_cal_obs(folder_name):
    results_folder_list = os.listdir(folder_name)
    results_folder_list = [os.path.join(os.path.abspath(folder_name),results_name) 
                            for results_name in results_folder_list]
    print(results_folder_list)
    results_tuple = [(os.path.abspath(folder),
                      os.path.join(os.path.abspath(folder), "{}.out".format(folder.split('/')[-1])))
                      for folder in results_folder_list]
    with Pool() as pool:
        pool.map(cal_obs, results_tuple)


def main():
    train_dir = "./data"
    #valid_dir = "./validation"
    #print("Generating events...")
    #run_event(train_dir)
    #print("Generating Done!")
    run_cal_obs(train_dir)
    print("Model observable calculation Done!")




if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print("It use {} seconds to do calculation".format(t2-t1))


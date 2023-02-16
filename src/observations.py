import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from scipy.stats import kstest, spearmanr, kurtosis, skew, entropy
from tqdm import tqdm

def binning_raw_data(x, y, n_bin) : 

    x_scale = np.logspace(np.log10(np.min(x)-0.1), np.log10(np.max(x) + 0.1), n_bin)
    bin_indptr = 0
    cur_x_axis = (x_scale[bin_indptr] + x_scale[bin_indptr + 1])/2
    x_scale_dict = dict()
    y_scale_dict = dict()
    
    for i in range((x.shape[0])) : 
        while True: 
            if ((x_scale[bin_indptr] <= x[i]) & (x[i] < x_scale[bin_indptr+1])) : # Hash to current bin
                break
            else : # Move one-step further
                bin_indptr += 1 
                cur_x_axis = (x_scale[bin_indptr] + x_scale[bin_indptr + 1])/2
        try : 
            x_scale_dict[cur_x_axis] += 1
            y_scale_dict[cur_x_axis] += y[i]
        except : 
            x_scale_dict[cur_x_axis] = 1
            y_scale_dict[cur_x_axis] = y[i]
    return_x = []
    return_y = []
    for i in list(x_scale_dict.keys()) : 
        return_x.append(i)
        return_y.append(y_scale_dict[i]/x_scale_dict[i])
    return np.log10(return_x), return_y

def give_binning_degree_transitivity(entireDeg, entireBN, entireBT, nbin) : 
    
    DegX = [0] * len(entireBT)
    TransY = [0] * len(entireBT)
    
    for i, key in enumerate(entireBT) : 
        DegX[i] = entireDeg[key]
        TransY[i] = entireBT[key]/entireBN[key]
        
    DF = pd.DataFrame({'deg' : DegX, 
                      'trans' : TransY}).groupby(by = ['deg'], as_index = False).mean()
    newX, newY = DF.deg.values, DF.trans.values
    
    return binning_raw_data(newX, newY, nbin)

def load_hypergraph(data_path, give_degree = True) : 
    
    file = open(data_path, 'r')
    Lines = file.readlines()
    Edge = []
    node_dict = dict()
    
    for line in Lines : 
        cur_e = set(map(int, line.replace('\n', '').split(',')))
        Edge.append(cur_e)
        if give_degree : 
            for v in cur_e : 
                try : 
                    node_dict[v] += 1
                except : 
                    node_dict[v] = 1
                    
    return Edge, node_dict

def observation1(real_data, gen_data = 'none', showing_type = 'real_world') : 
    
    if showing_type not in ['real_world', 'generated'] : 
        raise TypeError('Should be one of real-world and generated')
    
    if showing_type == 'real_world' : 
        file1 = open(real_data, 'r')
        Lines1 = file1.readlines()
        real_hyperwedges = [0.0] * len(Lines1)
        for ii, line in tqdm(enumerate(Lines1)) : 
            cur_pairs = line.replace('\n', '').split(',')
            wT = float(cur_pairs[2])
            real_hyperwedges[ii] = wT
        print("Real World Data : {0} | Computed Transitivity {1}".format(real_data, np.mean(real_hyperwedges)))
    
    elif showing_type == 'generated' : 
        
        for i, file_path in enumerate([real_data, gen_data]) : 
            file1 = open(file_path, 'r')
            Lines1 = file1.readlines()
            if i == 0 : 
                real_hyperwedges = [0.0] * len(Lines1)
            else : 
                gen_hyperwedges = [0.0] * len(Lines1)
            for ii, line in tqdm(enumerate(Lines1)) : 
                cur_pairs = line.replace('\n', '').split(',')
                wT = float(cur_pairs[2])
                if i == 0 : real_hyperwedges[ii] = wT
                else : gen_hyperwedges[ii] = wT
            if i == 0 : 
                print("Real World Data : {0} | Computed Transitivity {1}".format(real_data, np.mean(real_hyperwedges)))
            else : 
                print("Generated Data : {0} | Computed Transitivity {1}".format(gen_data, np.mean(gen_hyperwedges)))
        print("")
        print("D-Statistic between them : {0}".format(kstest(real_hyperwedges, gen_hyperwedges)[0]))
            
def observation2(data_name, result_name) : # Hyperwedge Level Observation
    
    hyperedge, _ = load_hypergraph(data_path = data_name, give_degree = False)
    
    file = open(result_name, 'r')
    Lines = file.readlines()
    
    BSize = [0] * len(Lines)
    Trans = [0.0] * len(Lines)
    
    for ii, line in tqdm(enumerate(Lines)) : 
        cur_pairs = line.replace('\n', '').split(',')
        L1 = hyperedge[int(cur_pairs[0])]
        L2 = hyperedge[int(cur_pairs[1])]
        wT = float(cur_pairs[2])
        bodyG = L1.intersection(L2)
        
        BSize[ii] = int(len(bodyG))
        Trans[ii] = wT
    
    print("Data Name : {0} | Correlation between body group size and transitivity : {1}".format(data_name, spearmanr(BSize, Trans)[0]))
    
def observation3(data_name, result_name) : # Node Level Observation
    
    hyperedge, node_dict = load_hypergraph(data_path = data_name, give_degree = True)
    
    n_body_v = dict()
    n_trans_v = dict()
    
    file = open(result_name, 'r')
    Lines = file.readlines()
    
    for ii, line in tqdm(enumerate(Lines)) : 
        cur_pairs = line.replace('\n', '').split(',')
        L1 = hyperedge[int(cur_pairs[0])]
        L2 = hyperedge[int(cur_pairs[1])]
        wT = float(cur_pairs[2])
        bodyG = L1.intersection(L2)
        
        for v in bodyG : 
            try : 
                n_body_v[v] += 1
                n_trans_v[v] += wT
            except : 
                n_body_v[v] = 1
                n_trans_v[v] = wT
                
    X, Y = give_binning_degree_transitivity(entireDeg = node_dict, entireBN = n_body_v, entireBT = n_trans_v, nbin = 10)
    plt.figure(figsize = (5,4))
    plt.plot(X, Y, color = 'dodgerblue', linewidth = 10)
    plt.show()
    
def observation4(result_name) :
    
    file = open(result_name, 'r')
    Lines = file.readlines()
    he_n_dict = dict()
    he_t_dict = dict()
    
    for ii, line in tqdm(enumerate(Lines)) : 
        cur_pairs = line.replace('\n', '').split(',')
        L1 = int(cur_pairs[0])
        L2 = int(cur_pairs[1])
        wT = float(cur_pairs[2])
        try : 
            he_n_dict[L1] += 1
            he_n_dict[L2] += 1
            he_t_dict[L1] += wT
            he_t_dict[L2] += wT
        except : 
            he_n_dict[L1] = 1
            he_n_dict[L2] = 1
            he_t_dict[L1] = wT
            he_t_dict[L2] = wT
            
    cur_max = 0
    cur_min = 0
    
    for v in he_n_dict : 
        curT = he_t_dict[v]/he_n_dict[v]
        if curT > cur_max : cur_max = curT
        if curT < cur_min : cur_min = curT
            
    print("Data Name : {0} | Range of Hyperedge Transitivity : {1}".format(result_name, cur_max - cur_min))
    
if __name__ == "__main__" : 
    
    parser = argparse.ArgumentParser("Reproducing observations of Paper")
    parser.add_argument("-obs", "--observation_type", default = 1, type = int, help = "Type of Observation")
    parser.add_argument("-obs_detail", "--observation_detail", default = 'real_world', type = str, help = "Details of Observation")
    parser.add_argument("-real_data_name", "--real_data", default = "datasets/email_enron_HE.txt", type = str, help = "Name of Real Dataset")
    parser.add_argument("-gen_data_name", "--gen_data", default = "generated/email_enron_gen_HE.txt", type = str, help = "Name of Generated Dataset")
    parser.add_argument("-real_result_name", "--real_result", default = "datasets/email_enron_HE_output.txt", type = str, help = "Result of Real Dataset")
    parser.add_argument("-gen_result_name", "--gen_result", default = "generated/email_enron_gen_HE_output.txt", type = str, help = "Result of Generated Dataset")
    
    args = parser.parse_args()
    
    if args.observation_type not in [1, 2, 3, 4] : 
        raise TypeError("This type of observation is not given.")
    if args.observation_detail not in ['real_world', 'generated'] : 
        raise TypeError("This type of data is not given.")
        
    observation_type = args.observation_type
    observation_detail = args.observation_detail
    real_data_name = args.real_data
    gen_data_name = args.gen_data
    real_data_result = args.real_result
    gen_data_result = args.gen_result
    
    if observation_type == 1 : # Observation 1
        observation1(real_data = real_data_result, gen_data = gen_data_result, showing_type = observation_detail) 
        
    elif observation_type == 2 : # Observation 2
        if observation_detail == 'real_world' : 
            observation2(data_name = real_data_name, result_name = real_data_result)
        else : 
            observation2(data_name = gen_data_name, result_name = gen_data_result)
        
    elif observation_type == 3 : # Observation 3
        if observation_detail == 'real_world' : 
            observation3(data_name = real_data_name, result_name = real_data_result)
        else : 
            observation3(data_name = gen_data_name, result_name = gen_data_result)
    
    elif observation_type == 4 : # Observation 4
        if observation_detail == 'real_world' : 
            observation4(result_name = real_data_result)
        else : 
            observation4(result_name = gen_data_result)
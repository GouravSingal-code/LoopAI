import numpy as np
import sys, env
sys.path.append('../')

def input_data(input_array, train_test):
    input_array = np.array(input_array)
    split_percentage = env.SPLIT_PERCENTAGE
    split_index = int(len(input_array) * split_percentage)
    train_x , test_x =np.split(input_array, [split_index])
    return train_x if train_test == 'train' else test_x


def output_data(output_array, train_test):
    output_array = np.array(output_array)
    split_percentage = env.SPLIT_PERCENTAGE    
    split_index = int(len(output_array) * split_percentage)
    train_y , test_y =np.split(output_array, [split_index])
    return train_y if train_test == 'train' else test_y




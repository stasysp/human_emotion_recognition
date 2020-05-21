import numpy as np
import pandas as pd
import os
from shutil import copy
from os import listdir
from os.path import isfile, join
import csv

labels = [
        'positive',
        'neutral',
        'negative',
        'skip',
        'speech',
        'unknown',
        ]

def get_dirs_tree(path_to_destination_dataset):
    dir_names = labels
    for name_dir in ['/train', '/val']:
        path_to_main_dirs = path_to_destination_dataset + name_dir
        try:
            os.makedirs(path_to_main_dirs)
        except OSError:
            print ("Directory %s already exist" % path_to_main_dirs)
        else:
            print ("Successfully created the directory %s" % path_to_main_dirs)
        for name_dir_emotions in dir_names:
            path_to_inner_dirs = path_to_main_dirs + "/" + name_dir_emotions
            try:
                os.makedirs(path_to_inner_dirs)
            except OSError:
                print ("Directory %s already exist" % path_to_inner_dirs)
            else:
                print ("Successfully created the directory %s" % path_to_inner_dirs)
    

def get_train_val(path_to_csv, path_to_dataset, path_to_destination_dataset, number_of_samples, number_of_samples_per_class, extension):
    number_of_pngs = {'val' : 0, 'train' : 0, 'positive' : 0, 'neutral' : 0, 'negative' : 0, 'skip' : 0, 'speech' : 0, 'unknown' : 0,}
    df = pd.read_csv(path_to_csv, encoding="Windows-1251")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    get_dirs_tree(path_to_destination_dataset)
    for index, row in df.iterrows():
        path_to_txt = path_to_dataset + row['path'][2:].replace('\\', '/')
        path_to_png = path_to_txt[:-3] + extension[1:]

        if (not os.path.exists(path_to_png) or (number_of_pngs[row['emotions']]>number_of_samples_per_class)):
            continue
        if (number_of_pngs['train'] + number_of_pngs['val'] > number_of_samples):
            break
        main_dir = 'val' if index % 3 == 0 else 'train'

        number_of_pngs[main_dir]+=1
        number_of_pngs[row['emotions']]+=1

        dest_file_path = path_to_destination_dataset + "/" + main_dir + "/" + row['emotions'] + "/"
        #print(row['emotions'], dest_file_path)
        copy(path_to_png, dest_file_path)
    print("Number of pngs copied to dataset: ")
    print(number_of_pngs)

def get_stat_from_initial_results(path_to_files):

    result_files = [f for f in listdir(path_to_files) if isfile(join(path_to_files, f))]
    stats = ['std', '25%', '50%', '75%']
    emotions = ['neutral', 'speech', 'skip', 'negative', 'positive', 'unknown']
    df_sum = pd.DataFrame(columns=emotions, index=['count', 'std', '25%', '50%', '75%'])
    df_sum.loc['count'] = df_sum.loc['count'].replace(np.nan, 0)

    for file in result_files:
        df = pd.read_csv(path_to_files + file, index_col=False)
        df.emotions = df.emotions.str.replace('\d+', '')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        #df.to_csv(path_to_files + file)
        for emotion in emotions:    
            emotion_index = df[df.emotions == emotion].describe().T['mean'].idxmax()
            row_value = df[df.emotions == emotion].describe()[emotion_index]

            df_sum.at['count', emotion] += row_value['count']
            for stat in stats:
                df_sum.at[stat, emotion] = np.nanmean([df_sum.at[stat, emotion], row_value[stat]])
    return df_sum

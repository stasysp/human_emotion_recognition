import numpy as np
import pandas as pd
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

import os
import pandas as pd
import csv

def get_csv_for_dataset(path_to_dir, path_to_out, verbose=False):
#    PATH = 'D:\\localNLP\\RussianNLP'
#    DIRNAME2 = 'public_youtube1120_mp3'
#    CSV_FILE2 = 'public_youtube1120_mp3.csv'

    #file_count = sum(len(files) for _, _, files in os.walk(r'D:\\localNLP\\RussianNLP\\asr_public_phone_calls_2'))
    #print("asr_public_phone_calls_2:", file_count)

    #file_count = sum(len(files) for _, _, files in os.walk(r PATH+DIRNAME2))
    #print("public_youtube1120_mp3:", file_count)

    text_list = []
    path_list = []
    os.chdir(path_to_dir)
    for root, dirs, files in os.walk(".", topdown = False):
        for name in files:
            path_to_file = os.path.join(root, name)
            if path_to_file.endswith(".txt"):
                if verbose:
                    print(path_to_file + " text: ")
                with open(path_to_file, "r", encoding='utf-8') as file:
                    text = file.read()
                    if verbose:
                        print(text)
                    text_list.append(text)
                    path_list.append(path_to_file)


    text_list = [line.rstrip() for line in text_list]
    #print(path_list, text_list)

    col1 = pd.Series(path_list)
    col2 = pd.Series(text_list)

    df = pd.DataFrame({'path':col1.reindex(col2.index), 'text':col2})

    df.to_csv(path_to_out, sep = ',', index = False, encoding='Windows-1251')

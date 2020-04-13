#!/usr/bin/env python
# coding: utf-8

# ## The letters 'a', 'd', 'f', 'h', 'n', 'sa' and 'su' represent 
# 'anger', 'disgust', 'fear', 'happiness', 'neutral', 'sadness' and 'surprise' emotion classes respectively.

# In[1]:


import numpy
from matplotlib import mlab
import matplotlib.pyplot as pyplot
import scipy.io.wavfile
from collections import defaultdict
from scipy import misc
import subprocess


# In[2]:


def get_wave_data(wave_filename):
    sample_rate, wave_data = scipy.io.wavfile.read(wave_filename)
    #assert sample_rate == SAMPLE_RATE, sample_rate
    if isinstance(wave_data[0], numpy.ndarray): # стерео
        wave_data = wave_data.mean(1)
    return wave_data
def show_specgram(wave_data):
    fig = pyplot.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.specgram(wave_data, NFFT=WINDOW_SIZE, noverlap=WINDOW_SIZE - WINDOW_STEP, Fs=SAMPLE_RATE)
    pyplot.show()


# In[3]:


SAMPLE_RATE = 9000 # Hz
WINDOW_SIZE = 2048 # размер окна, в котором делается fft
WINDOW_STEP = 512 # шаг окна
FOLDER_NAME = 'public_youtube1120/'
PATH = '/home/isedunov/pipeline/public_youtube1120/'
MP3 = '.mp3'
DOT_WAV = '.wav'
LOG_FILENAME = "log.txt"
PATH_TO_LOG = PATH + '../' + LOG_FILENAME

log_file = open(LOG_FILENAME, 'a')


# In[ ]:


import os
from matplotlib import pyplot
import matplotlib.pyplot as plt

PATH += FOLDER_NAME

list_of_grand_dir = os.listdir(PATH) 

def make_base():
    for grand_folder in list_of_grand_dir:
        list_of_dir = os.listdir(PATH + grand_folder)
        grand_path = PATH + grand_folder + '/'
        for folder in list_of_dir:
            #folder = list_of_dir[3]
            list_of_mp3 = os.listdir(grand_path + folder)
            list_of_mp3 = list(filter(lambda x: x.endswith(MP3), list_of_mp3))
            for mp3 in list_of_mp3:
                mp3_filename = grand_path + folder + '/' + mp3
                wav = mp3.split('.')[0] + DOT_WAV
                wave_filename = grand_path + folder + '/' + wav
                png_filename = wave_filename.split('.')[0] + '.png'
                if os.path.isfile(png_filename):
                    log_file.write(png_filename + " : exist yet!\n")
                else:
                    log_file.write(png_filename + '\n')
                    subprocess.call(['ffmpeg', '-i', mp3_filename, wave_filename])
                    wave_data = get_wave_data(wave_filename)
                    fig = pyplot.figure()
                    ax = fig.add_axes((0,0,1,1))
                    ax.specgram(wave_data, NFFT=WINDOW_SIZE, noverlap=WINDOW_SIZE - WINDOW_STEP, Fs=SAMPLE_RATE)

                    pyplot.axis([0, 25, 0, 4000])
                    pyplot.axis('off')
                    pyplot.savefig(png_filename) 
                    pyplot.close(fig)

                    
    log_file.close()

make_base()       

#/home/latna/jupyter/lib/python3.6/site-packages/matplotlib/pyplot.py:513: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`).
#  max_open_warning, RuntimeWarning)


# In[ ]:


make_base()


# 

# In[ ]:


SAMPLE_RATE = 9000 # Hz
WINDOW_SIZE = 2048 # размер окна, в котором делается fft
WINDOW_STEP = 512 # шаг окна

PATH = '/home/isedunov/pipeline/public_youtube1120/public_youtube1120/0'
FILENAME = '000f45f0543c'
mp3 = '.mp3'
wav = '.wav'
def test():
    wave_filename = PATH + '/00/' + FILENAME + wav
    mp3_filename = PATH + '/00/' + FILENAME + mp3
    subprocess.call(['ffmpeg', '-i', mp3_filename, wave_filename])

    wave_data = get_wave_data(wave_filename)
    print(wave_data)
    fig = pyplot.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.specgram(wave_data, NFFT=WINDOW_SIZE, noverlap=WINDOW_SIZE - WINDOW_STEP, Fs=SAMPLE_RATE)
    pyplot.axis([0, 25, 0, 4000])  
    pyplot.axis('off')
    pyplot.show()
    print(fig.get_size_inches()*fig.dpi)


# for work from Google Collab
# from google.colab import drive
# drive.mount('/MyDrv')
# !cp "/MyDrv/My Drive/research/public_youtube1120_mp3.csv" "."

# requirements
# !{sys.executable} -m pip install dostoevsky==0.1.2
# !{sys.executable} -m pip install folium==0.2.1
# !dostoevsky download vk-embeddings cnn-social-network-model
import sys
import csv
import numpy as np
import pandas as pd
from dostoevsky.tokenization import UDBaselineTokenizer, BaselineTokenizer
from dostoevsky.word_vectors import SocialNetworkWordVectores,  Word2VecContainer
from dostoevsky.models import SocialNetworkModel, BaseModel
from keras.preprocessing.sequence import pad_sequences 

class DostoevskyTokenizer():
    def __init__(self):
        self.filename = None

    def init_tokenizer(self):
        tokenizer = BaselineTokenizer()
        word_vectors_container = SocialNetworkWordVectores()

        self.model = SocialNetworkModel(
          tokenizer=tokenizer,
          word_vectors_container=word_vectors_container,
          lemmatize=False,
        )
    def predict(self, sentences):
        X = pad_sequences([
          self.model.word_vectors_container.get_word_vectors(
          self.model.tokenizer.split(sentence, lemmatize = self.model.lemmatize)
        ) for sentence in sentences
        ], maxlen = self.model.sentence_length, dtype='float32')

        Y = self.model.model.predict(X)

        return Y
    def load_main_file(self, filename, nrows = None):
        self.filename = filename
        self.nrows = nrows
        self.main_df = pd.read_csv(filename, encoding='Windows-1251', nrows=nrows)
        self.text = np.array(self.main_df.text.tolist())
        self.path = np.array(self.main_df.path.tolist())

    def get_files_with_predict(self, path_to_save="", start=0, step=10, bound=100000):
        if self.filename == None:
            print("Error! Please set filename by .load_main_file(filename, nrows=None)")
            return 1
        pred = []
        print(i)
        for i in range(0, self.nrows, step):
            sentences = self.text[i:i+step]

            Y = self.model.predict(sentences)

            if i + 1 % bound == 0 and i != 0:
                name_to_save = path_to_save + "result" + str(i - bound) + "-" + str(i) + ".csv"

                df_to_save = pd.DataFrame(pred)
                df_to_save['path'] = path[i-BOUND:i]
                df_to_save.to_csv(name_to_save, index=True)
                pred = []
            for y in Y:
                pred.append(y)
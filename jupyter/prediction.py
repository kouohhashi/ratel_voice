import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# This is a little hack. if we don't turn off stderr, we get error.
# python-shell catch the error.
import sys
stderr = sys.stderr
sys.stderr = open('/dev/null', 'w')

import numpy as np
from data_generator import AudioGenerator
from keras import backend as K
from utils import int_sequence_to_text

from keras.backend.tensorflow_backend import set_session
import tensorflow as tf

# import NN architectures for speech recognition
from sample_models import *

# This is a little hack. if we don't throw erro into /dev/null,
# finally back to stderr normal
sys.stderr = stderr

def get_predictions(audio_path, input_to_softmax, model_path):
    """ Print a model's decoded predictions
    Params:
        index (int): The example you would like to visualize
        partition (str): One of 'train' or 'validation'
        input_to_softmax (Model): The acoustic model
        model_path (str): Path to saved acoustic model's weights
    """

    # load the train and test data
    # if you are using spectrogram, change mfcc_dim
    data_gen = AudioGenerator(spectrogram=False, mfcc_dim=13)
    data_gen.load_train_data(desc_file='./jupyter/train_corpus.json')
    data_point = data_gen.normalize(data_gen.featurize(audio_path))
    # print(data_gen.feats_mean)
    # print(data_gen.feats_std)

    # # normalize data
    # data_point = data_gen.featurize(audio_path)
    # feats_mean = np.array([14.81652005, -0.1802923,  -1.22285122, 0.87062853, -16.05643781, -14.03943633, -5.7298706, -15.52425927, -3.39637537, -3.85226744, -5.17435844,  -2.13766871, -11.39111645])
    # feats_std = np.array([7.16816358, 14.58747728, 11.99928947, 15.69431836, 14.45918537, 16.79930368, 13.98395715, 12.60133111, 11.61310503, 11.34526655, 12.01205471, 13.41467652, 10.89021869])
    # eps = 1e-14
    # data_point = (data_point - feats_mean) / (feats_std + eps)


    # obtain and decode the acoustic model's predictions
    input_to_softmax.load_weights(model_path)
    prediction = input_to_softmax.predict(np.expand_dims(data_point, axis=0))
    output_length = [input_to_softmax.output_length(data_point.shape[0])]
    pred_ints = (K.eval(K.ctc_decode(
                prediction, output_length)[0][0])+1).flatten().tolist()

    recognized_text = "".join(int_sequence_to_text(pred_ints))
    print(recognized_text)
    # # play the audio file, and display the true and predicted transcriptions
    # print('-'*80)
    # # Audio(audio_path)
    # # print('True transcription:\n' + '\n' + transcr)
    # print('-'*80)
    # print('Predicted transcription:\n' + '\n' + ''.join(int_sequence_to_text(pred_ints)))
    # print('-'*80)



def main(argv):

    # if (argv)
    # argv_1 = argv[1]
    # print("argv_1: {}".format(argv_1))
    print("argv_1: {}".format( len(argv) ))
    # print("argv, len:{}".format(len(argv)))
    print("argv:{}".format(argv))

    # if len(argv) < 2:
    if len(argv) < 3:
        print("error")
        return

    # /home/kouohhashi/AIND-VUI-Capstone/samples/16/13/16-13-0000.wav
    audio_path = argv[1]
    print(audio_path)

    model_name = argv[2]
    print(model_name)
    # return;
    # print(get_predictions)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    # output_dim is up to languages 85
    get_predictions(audio_path=audio_path,
                    input_to_softmax=final_model(input_dim=13, # change to 13 if you would like to use MFCC features
                            filters=200,
                            kernel_size=11,
                            conv_stride=2,
                            conv_border_mode='valid',
                            units=200,
                            output_dim=29),
                    model_path=dir_path+'/results/'+model_name)

if __name__ == '__main__':
  main(sys.argv)

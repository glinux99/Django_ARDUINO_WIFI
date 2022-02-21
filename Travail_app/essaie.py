import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import spacy
import webbrowser
import urllib.request
import re
from fuzzywuzzy import fuzz
q = queue.Queue()
cool=[]
def tokenization(texte):
    cool=[]
    nlp = spacy.load('fr_core_news_md')
    texte = nlp(texte)
    for token in texte:
        cool.append(token.lemma_)
    cool=' '.join(cool)  
    return cool
q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "vosk-model-small-fr"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            help=1
            t=0 
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    sortie=json.loads(rec.FinalResult())
                else:
                    sortie=json.loads(rec.PartialResult())
                if( "partial" in str(sortie)):
                    sortie=sortie["partial"]
                    t+=1
                else:
                    sortie=sortie["text"]
                    t+=1
                    
                print(sortie)
                if dump_fn is not None:
                    dump_fn.write(data)

                if 'Erika' in rec.PartialResult() and help==1:
                        os.system('pico2wave -w erica.wav -l fr-FR "Oui patron" pitch -200 vol 5 && play erica.wav && rm erica.wav')
                        help=0    
                if 'allume lampe chambre Daniel' in rec.PartialResult() and help==1:
                        #urllib.request.urlopen('http://192.168.43.181/R10')
                        os.system('pico2wave -w erica.wav -l fr-FR "allumage de la lampe faite" pitch -200 vol 5 && play erica.wav && rm erica.wav')
                        help=0
                if 'éteindre' in rec.PartialResult() and help==0:
                        urllib.request.urlopen('http://192.168.43.181/R11')
                        os.system('pico2wave -l fr-FR -w erica.wav "Extinction de la lampe" pitch -200 vol 1.5 && aplay erica.wav && rm erica.wav')
                        help=1
                if 'quitte' in rec.PartialResult():
                        os.system('pico2wave -l fr-FR -w erica.wav "L\'application a ete interompu avec succès!!!" pitch -200 vol 1.5 && aplay erica.wav && rm erica.wav')
                        parser.exit(0)       
except KeyboardInterrupt:
    os.system('pico2wave -l fr-FR -w erica.wav "L\'application a ete interompu avec succès!!!" pitch -200 vol 1.5 && aplay erica.wav && rm erica.wav')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))

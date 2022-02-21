import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import webbrowser
import urllib.request
import re
import spacy
from fuzzywuzzy import fuzz
nlp = spacy.load('fr_core_news_md')
def token(text):
    doc = nlp(text)
    cool=[]
    for token in doc:
        cool.append(token.lemma_)
    cool=' '.join(cool)    
    return cool

q = queue.Queue()

def int_or_str(text):
    """fonction d'aide lorsque les arguments ne sont pas respectes"""
    try:
        return int(text)
    except ValueError:
        return text

def AppelRapide(donnee_d_entree, frames, tempsT, statusCheck):
    """ceci est appele a partir d'un fil separe pour chaque bloc"""
    if statusCheck:
        print(statusCheck, file=sys.stderr)
    q.put(bytes(donnee_d_entree))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='voir la liste des equipement audio et quitter')
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
    help='le fichier audio a debute avec l enregistrement')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='le chemin de votre model')
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
        print ("telecharger le model de votre langage sur https://alphacephei.com/vosk/models")
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
                            channels=1, AppelRapide=AppelRapide):
            print('#' * 80)
            print('debuter a parler')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            help=1
             
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    print(rec.Result())
                else:
                    print(rec.PartialResult())
                if dump_fn is not None:
                    dump_fn.write(data)
               
                if 'allumez' in rec.PartialResult() and help==1:
                        urllib.request.urlopen('http://192.168.43.181/R10')
                        os.system('pico2wave -w erica.wav -l fr-FR "allumage de la lampe faite" pitch -200 vol 5 && play erica.wav && rm erica.wav')
                        help=0
                if 'éteindre' in rec.PartialResult() and help==0:
                        urllib.request.urlopen('http://192.168.43.181/R11')
                        os.system('pico2wave -l fr-FR -w erica.wav "Extinction de la lampe" pitch -200 vol 1.5 && aplay erica.wav && rm erica.wav')
                        help=1
                if 'quitte' in rec.PartialResult():
                        parser.exit(0)
                       
except KeyboardInterrupt:
    os.system('pico2wave -l fr-FR -w erica.wav "L\'application a ete interompu avec succes!!!" pitch -200 vol 1.5 && aplay erica.wav && rm erica.wav')                  
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))

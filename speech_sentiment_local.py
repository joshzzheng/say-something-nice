import os
import json
import sys
import serial
import logging
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage

logger = logging.getLogger('candy_logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('candy.log')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

from say_something_nice.recorder import Recorder

def transcribe_audio(path_to_audio_file):
    username = os.environ.get("STT_USERNAME")
    password = os.environ.get("STT_PASSWORD")
    speech_to_text = SpeechToText(username=username,
                                  password=password)

    with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
        return speech_to_text.recognize(audio_file,
            content_type='audio/wav')

def get_text_sentiment(text):
    alchemy_api_key = os.environ.get("ALCHEMY_API_KEY")
    
    alchemy_language = AlchemyLanguage(api_key=alchemy_api_key)
    result = alchemy_language.sentiment(text=text)
    if result['docSentiment']['type'] == 'neutral':
        return 'netural', 0
    return result['docSentiment']['type'], result['docSentiment']['score']

def main():
    has_arduino = False
    if len(sys.argv) > 1 and sys.argv[1] == 'arduino':
        has_arduino = True

    recorder = Recorder("speech.wav")

    if has_arduino:
        # configure the serial connections (the parameters differs on the device you are connecting to)
        ser = serial.Serial(
            port='/dev/tty.usbmodem1421',
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
        ser.isOpen()
        ser.flush()

    print("Please say something nice into the microphone\n")
    recorder.record_to_file()

    print("Transcribing audio....\n")
    result = transcribe_audio('speech.wav')
    
    text = result['results'][0]['alternatives'][0]['transcript']
    print("Text: " + text + "\n")
    
    sentiment, score = get_text_sentiment(text)
    print(sentiment, score)

    logger.info(text + " - " + sentiment + " - " + str(score))

    if "watson" in text or "Watson" in text:
        if has_arduino:
            if score != 0:
                if float(score) > 0.4:
                    ser.write('p')
                else:
                    ser.write('n')

                ser.flush()
                ser.close()

if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    try:
        main()
    except:
        print("IOError detected, restarting...")
        main()

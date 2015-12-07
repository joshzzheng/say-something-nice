import os
import pyaudio
import wave
import json

from sys import byteorder
from array import array
from struct import pack
from os.path import join, dirname

from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in xrange(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in xrange(int(seconds*RATE))])
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)
        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 80:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def transcribe_audio(path):

    username = os.environ.get("BLUEMIX_USERNAME")
    password = os.environ.get("BLUEMIX_PASSWORD")
    speech_to_text = SpeechToText(username=username,
                                  password=password)

    '''
    with open(join(dirname(__file__), path), 'rb') as audio_file:
        return speech_to_text.recognize(audio_file,
            content_type='audio/wav')
    '''
    return "it's nice to meet you Watson"


def get_text_sentiment(apikey, text):
    '''
    # Base AlchemyAPI URL for targeted sentiment call
    alchemy_url = "http://access.alchemyapi.com/calls/text/TextGetTextSentiment"
    
    # Parameter list, containing the data to be enriched
    parameters = {
        "apikey" : apikey,
        "text"   : text,
        "outputMode" : "json",
        "showSourceText" : 1
        }

    try:
        results = requests.get(url=alchemy_url, params=urllib.urlencode(parameters))
        response = results.json()

    except Exception as e:
        print "Error while calling TextGetTargetedSentiment on Tweet (ID %s)" % tweet['id']
        print "Error:", e
        return

    if 'OK' != response['status'] or 'docSentiment' not in response:
        print "Problem finding 'docSentiment' in HTTP response from AlchemyAPI"
        print response
        print "HTTP Status:", results.status_code, results.reason
        print "--"
        return
    '''
    print(json.dumps(alchemy_language.language(url=url), indent=2))

    '''
    sentiment = response['docSentiment']['type']
    score = 0.
    if sentiment in ('positive', 'negative'):
        score = float(response['docSentiment']['score'])
    '''
    return sentiment, score


if __name__ == '__main__':
    alchemy_api_key = os.environ.get("ALCHEMY_API_KEY")
    print("Please say something nice into the microphone")
    record_to_file('speech.wav')
    print
    print "Transcribing audio..."
    print
    result = transcribe_audio('speech.wav')
    text = result['results'][0]['alternatives'][0]['transcript']
    print "Text: " + text
    print
    print "How do I feel about this?"
    #sentiment, score = get_text_sentiment(alchemy_api_key, text)
    #print sentiment, score
    print(json.dumps(alchemy_language.language(text=text), indent=2))



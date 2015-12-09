import os
from os.path import join, dirname

from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage

from say_something_nice.recorder import Recorder


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def transcribe_audio(path_to_audio_file):

    username = os.environ.get("BLUEMIX_USERNAME")
    password = os.environ.get("BLUEMIX_PASSWORD")
    speech_to_text = SpeechToText(username=username,
                                  password=password)

    '''
    with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
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
    recorder = Recorder("speech.wav")

    print("Please say something nice into the microphone")
    recorder.record_to_file()

    print
    print("Transcribing audio...")
    print
    
    result = transcribe_audio('speech.wav')
    text = result['results'][0]['alternatives'][0]['transcript']
    print("Text: " + text)
    print
    print("How do I feel about this?")
    #sentiment, score = get_text_sentiment(alchemy_api_key, text)
    #print sentiment, score
    print(json.dumps(alchemy_language.language(text=text), indent=2))



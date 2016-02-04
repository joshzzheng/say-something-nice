import os
from dotenv import load_dotenv
from watson_developer_cloud import AuthorizationV1 as WatsonAuthorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from flask import Flask

app = Flask(__name__)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

auth = WatsonAuthorization(username=os.environ.get("BLUEMIX_USERNAME"),
                           password=os.environ.get("BLUEMIX_PASSWORD"))

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/token")
def getToken():
    return auth.get_token(url=SpeechToText.default_url)

if __name__ == "__main__":
    app.run(debug=True)

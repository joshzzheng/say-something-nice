import os
import json
from dotenv import load_dotenv
from flask import Flask
from flask import request
from pymongo import MongoClient
from watson_developer_cloud import AuthorizationV1 as WatsonAuthorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))



alchemy = AlchemyLanguage(api_key=os.environ.get("ALCHEMY_API_KEY"))
# client  = MongoClient(os.environ.get("MONGODB_URI"))
app     = Flask(__name__, static_url_path="/static", static_folder="static")
auth    = WatsonAuthorization(
    username=os.environ.get("BLUEMIX_USERNAME"),
    password=os.environ.get("BLUEMIX_PASSWORD")
)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/token")
def getToken():
    return auth.get_token(url=SpeechToText.default_url)

@app.route("/sentiment", methods=["POST"])
def getSentiment():
    result      = alchemy.sentiment(text=request.form["transcript"])
    # # dump(result["docSentiment"])
    # return json.dumps(result)
    sentiment   = result["docSentiment"]["type"]

    if sentiment == "neutral":
        score = 0
    else:
        score = result["docSentiment"]["score"]

    return json.dumps({"sentiment": sentiment, "score": score})


if __name__ == "__main__":
    app.run(debug=True)

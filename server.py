import os
from watson_developer_cloud import AuthorizationV1 as WatsonAuthorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from flask import Flask

app = Flask(__name__)
auth = WatsonAuthorization(username=os.environ.get("BLUEMIX_USERNAME"),
                           password=os.environ.get("BLUEMIX_PASSWORD"))

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/token")
def getToken():
    authorization.get_token(url=SpeechToText.default_url)
    return "Hellodsfs"

if __name__ == "__main__":
    app.run()

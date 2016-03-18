# Say Something Nice

![Screenshot](http://i.imgur.com/1hPcd1O.png)

## Introduction
This the software used for in the *Watson Naughty-or-Nice Candy Machine*.  Here is the [complete tutorial on Medium](https://medium.com/@joshzheng/how-to-build-a-candy-machine-with-feelings-922285a475c8#.hncnebk0v) on how to put build the candy machine.

This is a simple Flask web application that uses the [Watson Speech to Text](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/speech-to-text.html) service for voice transcription and the [Watson AlchemyLanguage](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/alchemy-language.html) sentiment analysis to score the sentiment of the words.

The front end (client.js) uses the [Watson Javascript Speech To Text SDK](https://github.com/watson-developer-cloud/speech-javascript-sdk) to communicate with the Watson Speech to Text service via WebSocket.  The back end uses the [Watson Developer Cloud Python SDK](https://github.com/watson-developer-cloud/python-sdk) to access the AlchemyLanguage endpoints.


## Installation
There's no installation required.  Simply clone the repository to run the server on localhost.
You do, however, need to create your own .env file since  I use [python-dotenv](https://github.com/theskumar/python-dotenv) to manage my credentials. You .env file should look like this.

#### .env
`STT_USERNAME=*your watson speech to text service credential*`   
`STT_PASSWORD=*your watson speech to text service credential*`   
`ALCHEMY_API_KEY=*your alchemy api key*`

## To Run
`python server.py` if there is no Arduino board connected.

`python server.py arduino` if there is an Arduino board connected.

*Note: defaults to localhost:5000*

## License
This project is licensed under the terms of the **MIT** license. You can check out the full license [here](https://opensource.org/licenses/MIT).

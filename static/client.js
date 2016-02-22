var state                   = 'loading'
var model                   = 'en-US_BroadbandModel'
var sttToken                = null
var $recordButton           = document.getElementById('record')
var $stopButton             = document.getElementById('stop')
var $results                = document.getElementById('results')
var sttStream               = null

$recordButton.addEventListener('click', listen)
$stopButton.addEventListener('click', stop)

function listen() {
  if(!sttStream) {
    sttStream = WatsonSpeech.SpeechToText.recognizeMicrophone({
      token: sttToken,
      model: model,
      objectMode: true,
    })

    sttStream.on('data', onData)
  }


  $recordButton.disabled  = true
  $stopButton.disabled    = false
}

function stop() {
  $recordButton.disabled  = true
  $stopButton.disabled    = true

  if(sttStream) {
    sttStream.stop()
    sttStream = null
  }

  sentimentAnalysis($results.textContent)
}

function onData(data) {
  $results.textContent = arguments[0].alternatives[0].transcript
}

function sentimentAnalysis(transcript) {
  var xhr = new XMLHttpRequest()

  xhr.addEventListener('load', function(evt) {
    sentiment = JSON.parse(evt.target.responseText).sentiment

    if(sentiment === 'positive') {
      reset('green')
    } else if(sentiment === 'negative') {
      reset('red')
    } else {
      reset()
    }
  })

  var formData = new FormData()
  formData.append('transcript', transcript)

  xhr.open('POST', '/sentiment')
  xhr.send(formData)
}

function reset(backgroundColor) {
  state = 'ready'
  document.body.style.background = backgroundColor || 'none'
  $results.textContent = ''
  $recordButton.disabled  = false
  $stopButton.disabled    = true
}

function getToken() {
  var xhr = new XMLHttpRequest()

  xhr.addEventListener('load', function(evt) {
    sttToken = evt.target.responseText
    reset()
  })

  xhr.open('GET', '/token')
  xhr.send()
}

getToken()

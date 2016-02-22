var state                   = 'loading'
var model                   = 'en-US_BroadbandModel'
var sttToken                = null
var $recordButton           = document.getElementById('record')
var $stopButton             = document.getElementById('stop')
var $results                = document.getElementById('results')
var sttStream               = null
var isStopped               = false
var timeout                 = null

$recordButton.addEventListener('click', listen)
$stopButton.addEventListener('click', stop)

function listen() {
  clearTimeout(timeout)

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

  isStopped = true
  sentimentAnalysis($results.textContent)
}

function onData(data) {
  if(!isStopped) {
    $results.textContent = arguments[0].alternatives[0].transcript
  }
}

function sentimentAnalysis(transcript) {
  if(!transcript) {
    return reset()
  }

  var xhr = new XMLHttpRequest()

  xhr.addEventListener('load', function(evt) {
    sentiment = JSON.parse(evt.target.responseText).sentiment

    if(sentiment === 'positive') {
      reset('rgba(164,198,57,0.25)', true)
    } else if(sentiment === 'negative') {
      reset('rgba(255,76,76,0.25)', true)
    } else {
      reset('', true)
    }

    timeout = setTimeout(reset, 3000)
  })

  var formData = new FormData()
  formData.append('transcript', transcript)

  xhr.open('POST', '/sentiment')
  xhr.send(formData)
}

function reset(backgroundColor, keepText) {
  state = 'ready'
  isStopped = false
  document.body.style.background = backgroundColor || 'none'
  $recordButton.disabled  = false
  $stopButton.disabled    = true

  if(!keepText) {
    $results.textContent = ''
  }
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

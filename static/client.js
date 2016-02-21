var state                   = 'loading'
var model                   = 'en-US_BroadbandModel'
var sttToken                = null
var $button                 = document.getElementById('action')
var $results                = document.getElementById('results')
var sttStream               = null
var defaultButtonClassName  = 'h3 btn btn-primary mb4'
var defaultResultsClassName = ''

$button.addEventListener('click', function() {
  switch(state) {
    case 'ready':
      state               = 'recording'
      $button.textContent = 'Recording...'
      $results.className  = ''
      sttStream = WatsonSpeech.SpeechToText
        .recognizeMicrophone({
          token: sttToken,
          model: model,
          objectMode: true,
          outputElement: '#results',
        })

      break

    case 'recording':
      try {
        sttStream.stop()
      } catch(e) {

      }

      state               = 'analysing'
      $button.disable     = true
      $button.textContent = 'Sentiment Analysing...'
      sentimentAnalysis($results.textContent)
      break
  }
})

function sentimentAnalysis(transcript) {
  var xhr = new XMLHttpRequest()

  xhr.addEventListener('load', function(evt) {
    state               = 'ready'
    sentiment           = JSON.parse(evt.target.responseText).sentiment

    if(sentiment === 'positive') {
      $results.className = 'green'
    } else if(sentiment === 'negative') {
      $results.className = 'red'
    }

    $button.disabled    = false
    $button.textContent = 'Click to record'
  })

  var formData = new FormData()
  formData.append('transcript', transcript)

  xhr.open('POST', '/sentiment')
  xhr.send(formData)
}

function init() {
  var xhr = new XMLHttpRequest()

  xhr.addEventListener('load', function(evt) {
    state               = 'ready'
    sttToken            = evt.target.responseText
    $button.disabled    = false
    $button.textContent = 'Click to record'
    $results.className  = ''
  })

  xhr.open('GET', '/token')
  xhr.send()
}

init()

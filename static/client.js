var state                   = 'loading'
var model                   = 'en-US_BroadbandModel'
var sttToken                = null
var $button                 = document.getElementById('action')
var sttStream               = null
var defaultButtonClassName  = 'h3 btn btn-primary mb4'

$button.addEventListener('click', function() {
  switch(state) {
    case 'ready':
      state               = 'recording'
      $button.textContent = 'Recording...'
      sttStream = WatsonSpeech.SpeechToText
        .recognizeMicrophone({ token: sttToken, model: model })
        .on('result', onResult)
        .on('data', onFinish)
      break

    case 'recording':
      sttStream.stop()
      state               = 'waiting'
      $button.disable     = true
      $button.textContent = 'Waiting final results...'
      break
  }
})

function onResult(results) {
  document.getElementById('results').textContent = results.alternatives[0].transcript
}

function onFinish() {
  state               = 'ready'
  $button.disabled    = false
  $button.textContent = 'Click to record'
}

function init() {
  var xhr = new XMLHttpRequest()

  xhr.addEventListener('load', function(evt) {
    state               = 'ready'
    sttToken            = evt.target.responseText
    $button.disabled    = false
    $button.textContent = 'Click to record'
  })

  xhr.open('GET', '/token')
  xhr.send()
}

init()

// The following is from a tutorial from
// https://html5.tutorials24x7.com/blog/how-to-capture-image-from-camera
// This code is to experiment to be used for application.


// // Setting the up the variables that will be used.
// var startCap = d3.select('#btn-start');
// var stopCap = d3.select('#btn-stop');
// var capture = d3.select('#btn-capture');

// var stream = d3.select('#stream')
// var capture = d3.select('#capture')
// var snapshot = d3.select('#snapshot')

// // Video stream

// var cameraStream = null;

// // Listeners

// startCap.on('click', startStream);
// stopCap.on('click', stopStream)

// function startStream(){
//     var mediaSupport = 'mediaDevices' in navigator;

//     if (mediaSupport && null == cameraStream){
//         navigator.mediaDevices.getUserMedia( {video: true} )
//         .then(function(mediaStream){

//             cameraStream = mediaStream;
//             stream.srcObject = mediaStream;
//             stream.play();
//         })
//         .catch(function(err){
//             console.log("Unable to access Camera: " + err);
//         });
//     }
//     else{
//         alert('Your Browser does not support media devices.')

//         return;
//     }
// };

// function stopStream(){
//     if (null != cameraStream){
//         var track = cameraStream.getTracks()[0];

//         track.stop();
//         stream.load();

//         cameraStream = null;
//     }
// };

// function capture(){

// };

// The buttons to start & stop stream and to capture the image
var btnStart = document.getElementById( "btn-start" );
var btnStop = document.getElementById( "btn-stop" );
var btnCapture = document.getElementById( "btn-capture" );

// The stream & capture
var stream = document.getElementById( "stream" );
var capture = document.getElementById( "capture" );
var snapshot = document.getElementById( "snapshot" );

// The video stream
var cameraStream = null;

// Attach listeners
btnStart.addEventListener( "click", startStreaming );
btnStop.addEventListener( "click", stopStreaming );
btnCapture.addEventListener( "click", captureSnapshot );

// Start Streaming
function startStreaming() {

  var mediaSupport = 'mediaDevices' in navigator;

  if( mediaSupport && null == cameraStream ) {

    navigator.mediaDevices.getUserMedia( { video: true } )
    .then( function( mediaStream ) {

      cameraStream = mediaStream;

      stream.srcObject = mediaStream;

      stream.play();
    })
    .catch( function( err ) {

      console.log( "Unable to access camera: " + err );
    });
  }
  else {

    alert( 'Your browser does not support media devices.' );

    return;
  }
}

// Stop Streaming
function stopStreaming() {

  if( null != cameraStream ) {

    var track = cameraStream.getTracks()[ 0 ];

    track.stop();
    stream.load();

    cameraStream = null;
  }
}

function captureSnapshot() {

  if( null != cameraStream ) {

    var ctx = capture.getContext( '2d' );
    var img = new Image();

    ctx.drawImage( stream, 0, 0, capture.width, capture.height );
  
    img.src   = capture.toDataURL( "image/png" );
    img.width = 240;

    snapshot.innerHTML = '';

    snapshot.appendChild( img );
  }
}